"""
Ihmacs buffer implementation.
"""

from fundamental_mode import FundamentalMode
from tree_helpers import merge_trees


class Buffer:
    """
    Ihmacs text buffer.

    Attributes:
        _text: A string representing the buffer text.
        _modified: A bool representing if the buffer has been modified since
            last save.
        _point: An int representing cursor position in file.
        _mark: An int representing the mark position in file. Used to define
            the region.
        _name: A string representing the buffer name
        _path: A string representing the file path on the system associated
            with the buffer. This is the file the buffer is saved to.
        major_mode: A major mode type representing the active major mode.
        keymap: A dictionary tree representing the keymap for the buffer.
        _display_line: An int representing which line in the buffer is to be
            displayed as the first line of a window in the view. Line number
            indexes at 1, as in, the first line is 1 not 0.
        _read_only: A bool representing if the buffer is read only or not.
    """

    def __init__(self, name="**", path="", keymap=None,
                 read_only=False):
        """
        Initialize buffer instance.

        Args:
            name: Keyarg, a string representing the buffer name.
            path: Keyarg, a string representing the associated file path.
            keymap: The keymap to start off with. As this is a buffer, this is
                the global keymap passed through.
            read_only: A bool representing whether or not to make the new
                buffer read only.
        """
        self._text = ""
        self._modified = False
        self._point = 0
        self._mark = 0
        self._name = name
        self._path = path
        self._read_only = read_only

        self.major_mode = FundamentalMode()

        if keymap is None:
            keymap = {}
        # Need to write recursive tree merge.
        self.keymap = merge_trees(keymap, self.major_mode.modemap)

        # Index at 1 as Emacs and every other editor does for line number.
        self._display_line = 1

        # If path was passed load file
        # if self.path != "":
        # TODO: Add error handling for if the file does not exist yet
        # self.revert()

    # Properties
    @property
    def read_only(self):
        """
        Return read only status of buffer.
        """
        return self._read_only

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

    @property
    def display_line(self):
        """
        Return the display line for the buffer.
        """
        return self._display_line

    @property
    def line(self):
        """
        Return the line in the buffer the point is located at.
        """
        point = self.point
        text_before_point = self.text[:point]
        # Because of the bloody convention that the first line of text is 1 not
        # 0 add 1
        return 1 + text_before_point.count("\n")

    @property
    def column(self):
        """
        Return the column in the buffer the point is located at.
        """
        point = self.point
        text = self.text
        # Count how many characters it takes to find a newline char before
        # point
        col = 0
        while point - col > 0:
            if text[point-col-1] == "\n":  # Hard coding Unix newline...
                return col
            col += 1
        return col

    @property
    def line_count(self):
        """
        Return the number of lines in the buffer.
        """
        text = self.text
        return text.count("\n") + 1

    @property
    def modeline(self):
        """
        Generate buffer specific text to place on the modeline.

        Takes information about the buffer and creates two formatted strings to
        print at the left and right sides of the modeline.

        Returns:
            A tuple containing two strings. The first string is intended to be
            displayed at the left of the modeline, and the 2nd is intended to
            be displayed at the right of the modeline.
        """
        # Left Side
        line = self.line
        column = self.column
        modified = self.modified
        if modified:
            modified_status = "MODIFIED"
        else:
            modified_status = "SAVED"
        name = self.name
        total_lines = self.line_count
        scroll_percent = round(line/total_lines * 100)

        left = f"{line}:{column} {modified_status}   {name}   {scroll_percent}%"

        # Right Side
        major_mode = self.major_mode
        major_mode_name = major_mode.name

        right = f"{major_mode_name}"

        return (left, right)

    # Helper methods

    def _normalize_pos(self, pos):
        """
        Normalize a point to ensure it lies in the range of the buffer.

        The range of the buffer is from 0 to the length of the text.

        Args:
            pos: An int representing a point in the buffer.

        Returns:
            An int between 0 and the length of the text in the buffer.
        """
        return max(0, min(pos, len(self.text)))

    # Disk operations
    def revert(self):
        """
        Revert buffer by reloading associated file.

        Updates modified state to False.

        If the file does not exist, print error to *messages* buffer.

        Returns:
            A bool representing whether or not the revert was successful.
        """
        path = self.path
        with open(path, "r") as f:
            self._text = f.read()

        self._point = 0
        self._mark = 0
        self._modified = False

    def save_buffer(self):
        """
        Save modified buffer to associated path.

        Updates modified state to False.
        """
        path = self.path
        with open(path, "w") as f:
            f.write(self.text)

        self._modified = False

    def write_file(self, path):
        """
        Update associated path and write buffer to new associated path.

        Updates modified state to False.
        """
        with open(path, "w") as f:
            f.write(self.text)

        self._path = path
        self._modified = False
        # TODO: Update buffer name to the file name. I should look
        # into path handling in python so I don't end up hardcoding
        # with unix forward slashes.

    # Movement

    def set_point(self, pos):
        """
        Set point to position in buffer.

        Args:
           pos: An int representing where in the buffer to set point.
        """
        pos = self._normalize_pos(pos)
        self._point = pos

    def set_mark(self, pos):
        """
        Set mark to position in buffer.

        Args:
            pos: An int representing where in the buffer to set mark.
        """
        pos = self._normalize_pos(pos)
        self._mark = pos

    def scroll_buffer(self, lines):
        """
        Scroll buffer by N lines.

        Ensures that it will always be bound between 1 and the total number of
        lines.

        Args:
            lines: An int representing the number of lines to scroll buffer.
                Can be negative.
        """
        current_line = self.display_line
        total_lines = len(self.text.split("\n"))

        self._display_line = max(1, min(total_lines, current_line + lines))

    # Base editing operations. These all return values because that will
    # be useful for say, pushing to the kill ring.

    def insert(self, *args):
        """
        Insert args at point in buffer.

        Updates state of _text, _point, and _mark attributes.

        Does nothing if buffer is read only.

        Args:
            args: A tuple of strings to insert.

        Returns:
            A string representing the inserted text. Returns False if buffer
            is read only
        """
        if self.read_only:
            return False

        point = self.point
        mark = self.mark

        insert_text = "".join(args)
        insert_len = len(insert_text)

        # The side effects
        self._text = self.text[:point] + insert_text + self.text[point:]
        self._point = point + insert_len

        if mark > point:
            self._mark = mark + insert_len

        self._modified = True

        # Return inserted text
        return insert_text

    def delete_char(self, chars=1):
        """
        Delete characters from buffer at point.

        Updates state of _text, _point, and _mark attributes.

        Does nothing if buffer is read only.

        Args:
            chars: Number of characters to delete. If positive, delete
                characters after point. If negative, delete characters before
                point.

        Returns:
            A string containing the deleted text. False if buffer is read only.
        """
        if self.read_only:
            return False

        points = (self.point, self._normalize_pos(self.point + chars))

        # Rearrange due to negative args
        start = min(points)
        end = max(points)

        # Info about what we are deleting
        deleted_text = self.text[start:end]
        deleted_len = len(deleted_text)

        # The side effects
        self._text = self.text[:start] + self.text[end:]

        # If deleting text before point, move point backwards
        if chars < 0:
            self._point = start

        # Handle the mark, move as would be expected
        mark = self.mark

        if start <= mark <= end:
            self._mark = start
        elif mark > end:
            self._mark = mark - deleted_len

        self._modified = True

        # Return deleted text
        return deleted_text

    def delete_region(self):
        """
        Delete text in region defined by point and mark.

        Updates state of _text, _point, and _mark attributes.

        Does nothing if buffer is read only.

        Returns:
            A string containing all the deleted text. False if buffer is read
            only.
        """
        if self.read_only:
            return False

        start = min(self.point, self.mark)
        end = max(self.point, self.mark)

        deleted_text = self.text[start:end]

        # Side effects
        self._text = self.text[:start] + self.text[end:]
        self._point = start
        self._mark = start

        self._modified = True

        # Handle the return
        return deleted_text

    def append(self, text):
        """
        Append text to buffer without modifying point or mark.

        Does nothing if buffer is read only.

        Args:
            text: A string representing text to append to the buffer.

        Returns:
            A string representing the text appended to the buffer. False if
            buffer is read only.
        """
        self._text = self._text + text
        return text
