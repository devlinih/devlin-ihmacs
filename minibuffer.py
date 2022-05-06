"""
Minibuffer class and MinibufferMode for Ihmacs.

Minibuffer inherits from the Buffer class.

MinibufferMode is primarily designed for its keymap.
"""


import re

from buff import Buffer
from fundamental_mode import FundamentalMode
from tree_helpers import (
    replace_in_tree,
    merge_trees,
    build_tree_from_pairs,
    docstring_equal_p,
)
from basic_editing import (
    command_undefined,
    find_file,
    newline,
    scroll_up,
    scroll_down,  # Add more as I create and bind them
)


class MinibufferMode(FundamentalMode):
    """
    Minibuffer specific editing mode.

    Primarily exists to restrict the keymap. Unlike most modes, which will
    expand on the global keymap and the keymap provided by fundamental mode,
    minibuffer mode seeks remap commands that could potentially be dangerous
    when used in the minibuffer context.

    Attributes:
        _name: A string representing a printed name of the mode.
        _modemap: A dictionary of dictionaries representing the modemap. This
            is the keymap specific to the mode.
        _word_delimiters: A list of regular expressions used to represent what
            the word delimiters are for the given mode. This is a list because
            it's easier to expand or delete for other modes.
    """

    _name = "Minibuffer"

    def __init__(self, keymap=None):
        """
        Initialize Minibuffer mode.

        Args:
            keymap: A dictionary tree representing a keymap. Is optional;
                however, it's intended to pass the global keymap.
        """
        if keymap is None:
            keymap = {}

        # Unbind certain commands that when executed in the minibuffer will
        # cause disastrous effects (GNU/Emacs doesn't do this and let me tell
        # you, saving a minibuffer causes some weird stuff)
        functions_to_unbind = [find_file, scroll_up, scroll_down]
        for func in functions_to_unbind:
            # This does not work because all the functions in
            # functions_to_unbind point to a different place than the instances
            # of these functions in keymap. I have no idea how to get around this.
            keymap = replace_in_tree(keymap, func, command_undefined,
                                     test=docstring_equal_p)

        minibuffer_keymap = build_tree_from_pairs(
            [[["C-j"], minibuffer_exit]]
        )

        self._modemap = merge_trees(keymap, minibuffer_keymap)


class Minibuffer(Buffer):
    """
    Ihmacs Minibuffer.

    The minibuffer is an Emacs concept that is used to prompt for user input.
    It is a restricted version of a buffer that is displayed in the echo area.

    The minibuffer needs to be able to respond to typical editing commands, so
    all public attributes, properties, and public methods available to a
    regular buffer need to be available here, although their results may be
    different. Some public attributes of regular buffers that should be
    constants in the minibuffer are replaced with properties (e.g. the
    minibuffer has no minor modes so it has a minor mode property that always
    returns []).

    Attributes:
        _text: A string representing user inputted minibuffer text.
        _modified: A bool representing if the buffer has been modified.
        _point: An int representing the cursor position in the minibuffer.
        _mark: An int representing the mark position in the minibuffer.
        _name: A string representing the name of this minibuffer instance.
        _prompt: A string representing a prompt to display at the start of the
            minibuffer.
        major_mode: A major mode type representing the minibuffer's mode.
        keymap: A dictionary tree representing the keymap for the minibuffer.
    """

    def __init__(self, name="*minibuffer*", prompt="",
                 selections=None, keymap=None):
        """
        Initialize minibuffer instance.

        Args:
            name: Keyarg, a string representing the minibuffer name.
            prompt: Keyarg, a string representing the prompt to display at the
                start of the line.
            keymap: The keymap to start off with. As this is a buffer, this is
                the global keymap passed through.
            selections: An optional list of strings representing legal
                completions for minibuffer input. If nothing or None is passed,
                any string is a legal completion.
        """
        # Initialize a buffer
        super().__init__(name=name)

        self._prompt = prompt
        self.major_mode = MinibufferMode(keymap=keymap)

        if keymap is None:
            keymap = {}
        self.keymap = merge_trees(keymap, self.major_mode.modemap)

        self._selections = selections

    @property
    def selections(self):
        """
        Return the list of minibuffer selections.
        """
        return self._selections


def minibuffer_exit(ihmacs_state):
    """
    Exit minibuffer input if the minibuffer contains a valid selection.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.

    Returns:
        The minibuffer text. If the text is not a valid selection, return False.
    """
    # If this command is run, then the active buff is a minibuffer
    buff = ihmacs_state.active_buff

    text = buff.text
    selections = buff.selections

    # If there are no requires selection options
    if len(selections) == 0:
        return text

    # Handle selections
    if text in selections:
        return text

    return False
