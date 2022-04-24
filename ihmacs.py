"""
Class representing the top level of an Ihmacs session.
"""

from buffer import Buffer
import curses


class Ihmacs:
    """
    Class representing top level of an Ihmacs session.

    Attributes:
        kill_ring: A list (as a stack) of strings representing the kill ring.
            For those not familiar with Emacs reading this code, this is a
            clipboard, with infinite history of copies.
        buffers: List of all active buffers.
        keymap: A dictionary of dictionaries representing the global keymap.
        active_buffer: The active buffer.
        startup_directory: A string representing a path to the directory where
            Ihmacs was started.
    """

    def __init__(self, *files):
        """
        Initialize instance of Ihmacs.

        Args:
            files: A tuple of strings representing file paths to open as
                buffers.
        """
        self.kill_ring = []
        self.buffers = []
        self.keymap = {}
        self.startup_directory = "~/"  # TODO: actually make it do as labeled.

        # self.stdscr = (idk how I would do the ncurses window and all with
        # this)

        # self.active_buffer = # Bit confused about this. If I say
        # active_buffer is buffers[0] for example, will both active_buffer and
        # buffers[0] point to the same buffer object?  Or will it copy the
        # object and make my life harder?

        # Create scratch buffer and buffer for files specified on the command
        # line.

    def run(self):
        """
        Run the editor. Loop until exit.
        """
        pass
