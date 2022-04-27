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

    def __init__(self, window, buff, keychord):
        """
        Initialize controller.

        Args:
            window: The ncurses window.
            buff: The active buffer.
            keychord: The global keychord list, passed through.
        """
        self.window = window
        self.buff = buff
        self.keychord = keychord

    def read_key(self):
        """
        Read keychords from keyboard.

        Returns:
            An editing function that is mapped to in the keymap. If the
            user types an invalid keychord, it returns an editing function that
            prints invalid command.
        """
        pass

    def run_edit(self, func):
        """
        Run an editing function on the active buffer.

        Args:
            func: A function to run on the buffer.
        """
        pass
