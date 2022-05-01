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

    def __init__(self, ihmacs_state):
        """
        Initialize view.

        Args:
            ihmacs_state: The global state of the editor as an Ihmacs instance.
        """
        self.ihmacs_state = ihmacs_state

    def redraw_buffer(self):
        """
        Redraw the active buffer in the editing area.

        Completely erases the ncurses window and draws the text in the buffer
        in the editing area.
        """
        ihmacs_state = self.ihmacs_state
        window = ihmacs_state.window
        buff = ihmacs_state.active_buff
        # Line numbers index at 1, but Python indexes at 0.
        point_line = buff.line - 1
        point_col = buff.column
        text = buff.text
        # Line numbers index at 1, but Python indexes at 0.
        start_line = buff.display_line - 1

        # Get terminal size
        term_lines = curses.LINES
        term_cols = curses.COLS

        # Editing area is all but the last 2 lines
        display_lines = term_lines - 2

        # Draw text
        display_text = text.split("\n")[start_line:start_line+display_lines]
        window.erase()
        for line, text in enumerate(display_text):
            text = display_text[line]
            if len(text) > term_cols:
                text = text[:term_cols-1] + "$"
            window.addstr(line, 0, text)

        # Redraw line with point
        term_point_line = point_line-start_line
        point_line_text = display_text[term_point_line]

        if len(point_line_text) < term_cols:
            window.move(term_point_line, point_col)
        elif point_col < term_cols:
            window.move(term_point_line, point_col)
        elif point_col == len(point_line_text):
            start_index = point_col - term_cols + 2
            text = "$"+point_line_text[start_index:point_col]+" "
            window.addstr(term_point_line, 0, text)
            window.move(term_point_line, term_cols-1)
        else:
            start_index = point_col - term_cols + 2
            text = "$"+point_line_text[start_index:point_col]+"$"
            window.addstr(term_point_line, 0, text)
            window.move(term_point_line, term_cols-1)

        window.refresh()

    def echo(self, text):
        """
        Print text in the echo area.

        Args:
            text: A string representing text to print in the echo area.
        """
        ihmacs_state = self.ihmacs_state
        window = ihmacs_state.window

        # Get dimensions of terminal
        lines = curses.LINES
        columns = curses.COLS

        # Line to echo on, last line
        display_line = lines - 1

        # Get original location of cursor so we can return it
        cursor_pos = window.getyx()

        # Truncate the string if it is too long, adding indicator that it's
        # truncated.
        if len(text) > columns:
            text = text[:-3] + "..."

        window.addstr(display_line, 0, text)  # Echo at the bottom of the term
        window.move(cursor_pos[0], cursor_pos[1])  # Restore cursor
