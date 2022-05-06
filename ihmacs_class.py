"""
Class representing the top level of an Ihmacs session.
"""

import curses

from buff import Buffer
from view import View
from controller import Controller
from basic_editing import (
    command_undefined,
    DEFAULT_GLOBAL_KEYMAP,
)
from fundamental_mode import FundamentalMode


class Ihmacs:
    """
    Class representing top level of an Ihmacs session.

    Attributes:
        _buffers: List of all active buffers.
        _keymap: A dictionary of dictionaries representing the global keymap.
        _active_buff: An int representing the index of the active buffer.
        keychord: A list of strings representing the current keychord being
            inputted.
        end_session: A bool representing whether or not to continue the editing
            loop.
        kill_ring: A list (as a stack) of strings representing the kill ring.
            For those not familiar with Emacs reading this code, this is a
            clipboard, with infinite history of copies.
        echo: A string to display in the echo area.
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
        self._keymap = DEFAULT_GLOBAL_KEYMAP
        self._active_buff = 0
        self._buffers = []
        self.create_buffer(name="*scratch*")

        # This need to be mutated by the controller and are thus public.
        self.keychord = []
        self.end_session = False
        self.kill_ring = []
        self.echo = ""

        # The view and controller
        self._window = stdscr
        self.view = View(self)
        self.controller = Controller(self)

    @property
    def active_buff(self):
        """
        Return the active buffer.

        Does NOT return the index of the active buffer; rather, it returns the
        actual buffer object.

        If the buffer list is empty, create a new scratch buffer and return it.

        If the index is invalid, set the active buffer to be the last buffer in
        the list.

        Returns:
            A buffer object representing the active buffer.
        """
        if len(self._buffers) == 0:
            self.create_buffer(name="*scratch*")

        if self.active_buff_index >= len(self._buffers):
            self._active_buff = len(self._buffers) - 1

        return self._buffers[self._active_buff]

    @property
    def active_buff_index(self):
        """
        Return the index of the active buffer.
        """
        return self._active_buff

    @property
    def buffers(self):
        """
        Return the list of buffers.
        """
        return self._buffers

    @property
    def keymap(self):
        """
        Return the global keymap.
        """
        return self._keymap

    @property
    def window(self):
        """
        Return the main ncurses window.
        """
        return self._window

    @property
    def term_size(self):
        """
        Return terminal size.

        Updates

        Return a tuple of two ints representing the terminal size as (y, x)
        """
        return (curses.LINES, curses.COLS)

    # Helper methods
    def create_buffer(self, name="", path=""):
        """
        Create a new buffer and append it to the list of buffers.

        Sets the active buffer index to the index of the new buffer.

        Args:
            name: The name of the new buffer.
            major_mode: The major mode of the new buffer.
        """
        buffer_list = self._buffers
        new_buffer = Buffer(name=name,
                            path=path,
                            keymap=self._keymap)
        buffer_list.append(new_buffer)
        self._active_buff = len(buffer_list) - 1

    def switch_buffer(self, index):
        """
        Switch to the buffer located at index.

        If the index is invalid for the list active_buffers, do nothing.

        Args:
            index: An int representing the index of the buffer to change to.
        """
        buffer_list = self.buffers
        if 0 <= index < len(buffer_list):
            self._active_buff = index

    def kill_buffer(self, index):
        """
        Kill the buffer at index.

        If the index is invalid, do nothing.
        """
        buffer_list = self._buffers
        if 0 <= index < len(buffer_list):
            del buffer_list[index]

    # Main loop

    def run(self):
        """
        Run the editor. Loop until exit.
        """
        view = self.view
        controller = self.controller
        keymap = self.keymap  # This is just the global keymap
        keychord = self.keychord

        # Loop
        while not self.end_session:
            # Update display
            view.refresh_screen()

            # Read input
            keymap = self.active_buff.keymap

            keychord.clear()
            func = False
            while not callable(func):
                # Update echo area
                view.echo()

                # Read keystrokes
                controller.read_key()
                # Test for mapping
                func = read_keychord_keymap(keychord, keymap)
                # Echo the current keychord
                controller.echo(" ".join(keychord))

            # Clear echo area
            controller.echo("")

            # Act on input
            controller.run_edit(func)


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
        the mapping is undefined, or False if the keychord is an incomplete
        mapping.
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
