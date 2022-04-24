"""
Ihmacs buffer implementation.
"""


class Buffer:
    """
    Ihmacs text buffer.

    Attributes:
        text: A string representing the buffer text.
        modified: A bool representing if the buffer has been modified since
            last save.
        point: An int representing cursor position in file.
        mark: An int representing the mark position in file. Used to define
            the region.
        name: A string representing the buffer name
        path: A string representing the file path on the system associated with
            the buffer. This is the file the buffer is saved to.
        major_mode: A major mode type representing the active major mode.
        minor_modes: A list of minor modes representing the active minor modes.
        keymap: not decided yet, but a sort of tree structure mapping inputted
            keychords to editing methods. Are first class methods a thing or am
            I about to put myself into a world of hell?
        command_history: A list of functions/methods that have been executed
            since last save.
        modeline: A string who's format method will generate a modeline. It can
            display information about the buffer as well as information about
            active modes by their "lighter" string.
        display_line: An int representing which line in the buffer is to be
            displayed as the first line of a window in the view.
    """

    def __init__(self, name="**", path=""):
        """
        Initialize buffer instance.

        Args:
            name: Keyarg, a string representing the buffer name.
            path: Keyarg, a string representing the associated file path.
        """
        self._text = ""
        self._modified = False
        self._point = 0
        self._mark = 0
        self._name = name
        self._path = path
        # self.major_mode = instance of fundamental mode
        self.minor_modes = []
        # self.keymap = dict of dicts, I'll get to this when I get to this.
        self.command_history = []
        self.modeline = ""
        self.display_line = 0

        # If path was passed load file
        if self.path != "":
            # TODO: Add error handling for if the file does not exist yet
            self.revert()

    # Properties
    @property
    def text(self):
        """
        Return text in buffer.
        """
        return self._text

    @property
    def modified(self):
        """
        Return modification state of buffer.
        """
        return self._modified

    @property
    def point(self):
        """
        Return position of point in buffer.
        """
        return self._point

    @property
    def mark(self):
        """
        Return position of mark in buffer.
        """
        return self._mark

    @property
    def name(self):
        """
        Return name of buffer.
        """
        return self._name

    @property
    def path(self):
        """
        Return associated file path of buffer.
        """
        return self._path

    # Disk operations
    def revert(self):
        """
        Revert buffer by reloading associated file.

        If the file does not exist, print error to *messages* buffer.

        Returns:
            A bool representing whether or not the revert was successful.
        """
        pass

    def save_buffer(self):
        """
        Save modified buffer to associated path.

        Updates modified state to False.
        """
        pass

    def write_file(self, path):
        """
        Update associated path and write buffer to new associated path.

        Updates modified state to False.
        """
        pass

    # Movement
    def move_point(self, chars):
        """
        Move point N chars.

        Args:
            Chars: An int representing number of chars to move point.
        """
        pass

    def set_point(self, pos):
        """
        Set point to position in buffer.

        Args:
           pos: An int representing where in the buffer to set point.
        """
        pass

    def set_mark(self, pos):
        """
        Set mark to position in buffer.

        Args:
            pos: An int representing where in the buffer to set mark.
        """
        pass

    # Base editing operations

    # Note, these are the methods to manipulate the buffer. The editing
    # commands defined at a higher will have the same names, but when
    # calling this method will pass point and mark to these functions.

    def insert(self, pos, *args):
        """
        Insert args at position in buffer.

        Args:
            pos: An int representing position in buffer to insert at.
            args: A tuple of strings to insert.
        """
        pass

    def delete_char(self, pos, chars=1):
        """
        Delete characters at position from buffer.

        Args:
            pos: An int representing position in buffer to delete at.
            chars: Number of characters to delete. If positive, delete
                characters after point. If negative, delete characters before
                point.
        """
        pass

    def kill_region(self, start, end):
        """
        Kill text and push to kill ring.

        Args:
            start: An int representing the start bound for the region.
            end: An int representing the end obund for the region.
        """
        pass
