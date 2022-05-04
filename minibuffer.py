"""
Minibuffer class and MinibufferMode for Ihmacs.

Minibuffer inherits from the Buffer class.

MinibufferMode is primarily designed for its keymap.
"""


import re


from buff import Buffer
from fundamental_mode import FundamentalMode


class MinibufferMode(FundamentalMode):
    """
    Minibuffer specific editing mode.

    Primarily exists to restrict the keymap. Unlike most modes, which will
    expand on the global keymap and the keymap provided by fundamental mode,
    minibuffer mode seeks remap commands that could potentially be dangerous
    when used in the minibuffer context.
    """

    _name = "Minibuffer"

    def __init__(self):
        pass


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
        _keymap: A dictionary tree representing the keymap for the minibuffer.
    """

    def __init__(self, name="*minibuffer*", prompt="", keymap=None):
        """
        Initialize minibuffer instance.

        Args:
            name: Keyarg, a string representing the minibuffer name.
            prompt: Keyarg, a string representing the prompt to display at the
                start of the line.
            keymap: The keymap to start off with. As this is a buffer, this is
                the global keymap passed through.
        """
        # Initialize a buffer
        super.__init__(name="minibuffer", keymap)

        self._prompt = prompt
        self.major_mode = MinibufferMode()

        if keymap is None:
            keymap = {}
        # Need to write recursive merge
        self._keymap = keymap | self._major_mode.modemap
