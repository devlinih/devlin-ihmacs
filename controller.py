"""
Ihmacs controller module.

Has facilities for reading keychords and executing the associated command.
"""

import curses


class Controller:
    """
    Ihmacs class for handling input and executing actions.

    Attributes:
        window: The ncurses window we are reading from.
        buff: The active buffer.
        keychord: The global keychord.
    """

    def __init__(self, **ihmacs_state):
        """
        Initialize controller.

        Args:
            **keyargs: A keyarg list containing the entire global Ihmacs state.
        """
        # Frequently used things in the controller, saved for convenience.
        self.window = ihmacs_state["window"]
        self.buff = ihmacs_state["active_buff"]
        self.keychord = ihmacs_state["keychord"]

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

        # Read a keystroke. I am not an ncurses expert nor a c programmer so
        # this is probably an awful way of doing this. Fully except that this
        # code is garbage.
        ch1 = window.getch()
        key = ch1
        meta = ""
        if ch1 == 27:  # ALT (META) was pressed
            window.nodelay(True)
            ch2 = window.getch()  # Key pressed after alt
            key = ch2
            meta = "M-"
            window.nodelay(False)
            if ch2 == -1:  # Invalid key combination, hey idk curses is cursed
                return

        # Convert the key into a bytestring that's a printable
        # representation of the keystroke.
        unctrl = curses.keyname(key)

        # Check if control is pressed
        if len(unctrl) > 1:
            control = "C-"
            # Downcase so it works with the Emacs
            char = chr(unctrl[1]).lower()
            # convention of C-c instead of C-C
        else:
            control = ""
            char = chr(unctrl[0])

        # Side Effects
        keychord.append(control+meta+char)

    def run_edit(self, func):
        """
        Run an editing function on the active buffer.

        Args:
            func: A function to run on the buffer.
        """
        ihmacs_state = self.ihmacs_state

        func(ihmacs_state)
