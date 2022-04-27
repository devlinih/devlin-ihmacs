"""
Class representing the top level of an Ihmacs session.
"""

from buff import Buffer
from view import View
from controller import Controller

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
        keychord: A list of strings representing the current keychord being
            inputted.
        window: The global ncurses window.
        view: The view in the MVC architecture.
        controller: The controller in the MVC architecture.
    """

    def __init__(self, stdscr, *files):
        """
        Initialize instance of Ihmacs.

        Args:
            *files: A tuple of strings representing file paths to open as
                buffers.
        """
        self.kill_ring = []
        self.buffers = [Buffer("*scratch*")]
        self.active_buff = self.buffers[0]
        self.keymap = {}
        self.startup_directory = "~/"  # TODO: actually make it do as labeled.
        self.keychord = []
        self.window = stdscr
        self.view = View(self.window, self.active_buff)
        self.controller = Controller(
            self.window, self.active_buff, self.keychord)

        # Create scratch buffer and buffer for files specified on the command
        # line.

    def run(self):
        """
        Run the editor. Loop until exit.
        """
        view = self.view
        buff = self.active_buff

        char = ""
        while char != "~":
            view.redraw_buffer()
            char = self.window.getkey()
            buff.insert(char)
