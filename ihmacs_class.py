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
        _buffers: List of all active buffers.
        _keymap: A dictionary of dictionaries representing the global keymap.
        _active_buff: An int representing the index of the active buffer.
        _startup_directory: A string representing a path to the directory where
            Ihmacs was started.
        keychord: A list of strings representing the current keychord being
            inputted.
        end_session: A bool representing whether or not to continue the editing
            loop.
        _window: The global ncurses window.
        view: The view in the MVC architecture.
        controller: The controller in the MVC architecture.
    """

    def __init__(self, stdscr, *files):
        """
        Initialize instance of Ihmacs.

        Args:
            stdscr: The main ncurses window. Argument exists so curses.wrapper
                can pass it a window.
            *files: A tuple of strings representing file paths to open as
                buffers.
        """
        # Global editor state
        self._buffers = [Buffer("*scratch*")]
        self._active_buff = 0
        self._keymap = DEFAULT_GLOBAL_KEYMAP
        self._startup_directory = "~/"  # TODO: actually make it do as labeled.

        # This need to be mutated by the controller and are thus public.
        self.keychord = []
        self.end_session = False
        self.kill_ring = []

        # The view and controller
        self._window = stdscr
        self.view = View(self)
        self.controller = Controller(self)

    @property
    def buffers(self):
        """
        Return the list of all buffers.
        """
        return self._buffers

    @property
    def active_buff(self):
        """
        Return the active buffer.

        Does NOT return the index of the active buffer.

        Returns:
            A buffer object representing the active buffer.
        """
        return self._buffers[self._active_buff]

    @property
    def keymap(self):
        """
        Return the global keymap.
        """
        return self._keymap

    @property
    def startup_directory(self):
        """
        Return the startup directory of the editor.
        """
        return self._startup_directory

    @property
    def window(self):
        """
        Return the main ncurses window.
        """
        return self._window

    # Main loop

    def run(self):
        """
        Run the editor. Loop until exit.
        """
        view = self.view
        controller = self.controller
        keymap = self.keymap
        keychord = self.keychord

        # Loop
        while not self.end_session:
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

            # If point has moved, make sure it lies within an allowed range.


def read_keychord_keymap(keychord, keymap):
    """
    Find the function that a keychord maps to in a keymap.

    If the keychord does not terminate at a function, returns None.

    If the keychord has an undefined mapping, return command_undefined(from
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
