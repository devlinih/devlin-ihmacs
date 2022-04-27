"""
Ihmacs view module.

Views the active buffer.
"""

import curses


class View:
    """
    Ihmacs class for displaying text in a terminal.

    Attributes:
        window: The global ncurses window.
        buff: The active buffer.
    """

    def __init__(self, window, buff):
        """
        Initialize view.

        Args:
            window: The ncurses window.
            buff: The active buffer.
        """
        self._window = window
        self._buff = buff

    def redraw_buffer(self):
        """
        Redraw the buffer.
        """
        window = self._window
        buff = self._buff
        window.erase()
        window.addstr(0, 0, buff.text)
        window.refresh()
