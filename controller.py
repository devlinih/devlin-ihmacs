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
            window: The global ncurses window.
            buff: The active buffer.
            keychord: The global keychord list, passed through.
        """
        self.window = window
        self.buff = buff
        self.keychord = keychord

    def read_key(self):
        """
        Read key from the user.

        Appends the read key to the global keychord.
        """
        window = self.window
        keychord = self.keychord

        # Side Effects
        char = window.getkey()
        keychord.append(char)

    def run_edit(self, func):
        """
        Run an editing function on the active buffer.

        Args:
            func: A function to run on the buffer.
        """
        buff = self.buff
        keychord = self.keychord

        func(buff, keychord)
