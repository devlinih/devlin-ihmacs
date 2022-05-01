"""
Ihmacs controller module.

Has facilities for reading keychords and executing the associated command.
"""

from basic_editing import scroll_up

import curses


class Controller:
    """
    Ihmacs class for handling input and executing actions.

    Attributes:
        window: The ncurses window we are reading from.
        buff: The active buffer.
        keychord: The global keychord.
        ihmacs_state: The global state of the editor
    """

    def __init__(self, ihmacs_state):
        """
        Initialize controller.

        Args:
           ihmacs_state: An Ihmacs instance, the global state of the editor.
        """
        # Frequently used things in the controller, saved for convenience.
        self.window = ihmacs_state.window
        self.buff = ihmacs_state.active_buff
        self.keychord = ihmacs_state.keychord

        # The entire global state, used less frequently
        self.ihmacs_state = ihmacs_state

    def read_key(self):
        """
        Read keystroke from the user.

        A stroke is a single sequence, so an alphanumeric plus modifier keys.

        This will be appended to the global keychord in a string form.

        Appends the read key to the global keychord.
        """
        window = self.window
        keychord = self.keychord

        # Read keystroke. This code is designed to work whether keypad is
        # enabled or not.

        # Note: Pressing ESC yields some funky results with this code. It's
        # treated like a sticky keys version of meta. Unfortunately, it can
        # chain into itself, which would be confusing.
        key = []
        char = window.getch()
        key.append(char)

        while char != -1:
            window.nodelay(True)
            char = window.getch()
            key.append(char)

        window.nodelay(False)

        # I know comment rants are not good style, but it's kind of
        # needed to understand why the following code is the way it is.

        # Convert the raw key array into a string that's human readable and
        # consistent with the keymap dictionary.

        # This portion of the code assumes keypad is enabled. I gave up trying
        # to understand exactly how the terminal input was functioning, hence
        # went to keypad.

        # Unfortunately, this results in a few issues. Here's a brief list:
        # First, ESC (as well as C-3) is treated the same as meta, just a
        # sticky keys variant of it. It sends an escape code. Second, there is
        # no difference between C-j and RET, C-i and TAB, etc. Third, don't
        # even think about trying to decipher C- combinations that in the
        # number row.

        # Key was pressed with meta/ESC
        if key[0] == 27:
            meta = "M-"
            facekey = key[1]
        else:
            meta = ""
            facekey = key[0]

        # Handle key characters.

        # C-letter is reported as being from 1-26
        control = ""

        if facekey == 0:  # Apparently C-SPACE returns this
            facekey = " "
            control = "C-"
        elif 1 <= facekey <= 26:
            control = "C-"
            facekey = chr(curses.unctrl(facekey)[1]).lower()  # Extract letter
        elif 32 <= facekey <= 126:  # Alphanumeric keys, standard ASCII
            facekey = chr(facekey)
        elif facekey == 127:  # DEL (backspace)
            facekey = "DEL"
        elif 128 <= facekey <= 255:  # Extended ASCII. Maybe your kbd has this?
            facekey = chr(facekey)
        elif facekey > curses.KEY_MIN:  # keypad keys.
            facekey = curses.keyname(facekey).decode("utf-8")

        # Side Effects
        keychord.append(control+meta+facekey)

    def run_edit(self, func):
        """
        Run an editing function on the active buffer.

        If point moved, ensure it lies within a valid range of the view.

        Args:
            func: A function to run on the buffer.
        """
        ihmacs_state = self.ihmacs_state
        func(ihmacs_state)

        # Ensure point lies within a valid range of the view.
        self.ensure_valid_point()

    def ensure_valid_point(self):
        """
        Ensure point lies within a valid range of the view.

        If point has moved during editing such that it is out of view, scroll
        the buffer accordingly.
        """
        ihmacs_state = self.ihmacs_state
        buff = ihmacs_state.active_buff

        # Check that point is on a line within the view area
        view_min = buff.display_line
        view_max = view_min + curses.LINES - 2
        current_line = buff.line

        if current_line < view_min:
            buff.scroll_buffer(current_line-view_min)
        if current_line >= view_max:
            buff.scroll_buffer(current_line-view_max+1)
