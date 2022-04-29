"""
Class representing the top level of an Ihmacs session.
"""

from buff import Buffer
from view import View
from controller import Controller
from constants import DEFAULT_GLOBAL_KEYMAP
from basic_editing import *

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
        # Global editor state
        self.kill_ring = []
        self.buffers = [Buffer("*scratch*")]
        self.active_buff = self.buffers[0]
        self.keymap = DEFAULT_GLOBAL_KEYMAP
        self.startup_directory = "~/"  # TODO: actually make it do as labeled.
        self.keychord = []

        # The view and controller
        self.window = stdscr
        self.view = View(self.window, self.active_buff)
        self.controller = Controller(self.window,
                                     self.active_buff,
                                     self.keychord)

    def run(self):
        """
        Run the editor. Loop until exit.
        """
        view = self.view
        controller = self.controller
        keymap = self.keymap
        keychord = self.keychord

        # Loop
        while True:
            # Update display
            view.redraw_buffer()

            # Read input
            keychord.clear()
            func = False
            while not callable(func):
                controller.read_key()
                func = read_keychord_keymap(self.keychord, keymap)

            # Act on input
            controller.run_edit(func)


def read_keychord_keymap(keychord, keymap):
    """
    Find the function that a keychord maps to in a keymap.

    If the keychord does not terminate at a function, returns None.

    If the keychord has an undefined mapping, return command_undefined (from
    basic editing)

    Args:
        keychord: A list representing a keychord.
        keymap: A dictionary representing a keymap.

    Returns:
        A function representing a mapping, a the command_undefined function if
        the mapping is undefined, or False if the keychord is an incomplete mapping.
    """
    # If "keymap" is a function, return it
    if callable(keymap):
        return keymap

    # If they keychord is empty, the map is incomplete.
    if len(keychord) == 0:
        return False

    # If there is still input in the keychord, call recursively
    key = keychord[0]
    # Find what it maps to. If it maps to nothing, it maps to command_undefined
    value = keymap.get(key, command_undefined)
    return read_keychord_keymap(keychord[1:], value)
