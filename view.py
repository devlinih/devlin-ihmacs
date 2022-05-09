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

    def refresh_screen(self):
        """
        Redraw the active buffer and the modeline.

        Completely erases ncurses window before drawing text. Then refreshes
        the window.
        """
        curses.update_lines_cols()
        ihmacs_state = self.ihmacs_state
        window = ihmacs_state.window

        window.erase()
        self._redraw_buffer()
        self._draw_modeline()
        window.refresh()

    # pylint: disable=R0914
    def _redraw_buffer(self):
        """
        Redraw the active buffer in the editing area.

        Completely erases the ncurses window and draws the text in the buffer
        in the editing area.
        """
        ihmacs_state = self.ihmacs_state
        window = ihmacs_state.window
        buff = ihmacs_state.active_buff()
        # Line numbers index at 1, but Python indexes at 0.
        point_line = buff.line - 1
        point_col = buff.column
        text = buff.text
        # Line numbers index at 1, but Python indexes at 0.
        start_line = buff.display_line - 1

        # Get terminal size
        term_lines, term_cols = ihmacs_state.term_size

        # Editing area is all but the last 2 lines
        display_lines = term_lines - 2

        # Draw text
        display_text = text.split("\n")[start_line:start_line+display_lines]
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

    def _draw_modeline(self):
        """
        Draw the modeline for the active buffer.

        Does not clear the screen, assumed to be run after the screen is
        cleared.
        """
        ihmacs_state = self.ihmacs_state
        window = ihmacs_state.window
        buff = ihmacs_state.active_buff()
        modeline_left, modeline_right = buff.modeline

        # Get terminal size
        term_lines, term_cols = ihmacs_state.term_size

        # Get position of cursor to restore later
        cursor_y, cursor_x = window.getyx()

        # Find number of spaces needed to pad
        padding = term_cols - (len(modeline_left) + len(modeline_right))

        # Display the modeline on the 2nd to last line
        modeline = modeline_left + " "*padding + modeline_right
        if len(modeline) > term_cols:  # Truncate if too long
            modeline = modeline[:term_cols-3] + "..."
        window.addstr(term_lines-2, 0, modeline,
                      curses.A_REVERSE)

        # Restore position of cursor
        window.move(cursor_y, cursor_x)

    def echo(self):
        """
        Print the echo string in the echo area.

        Args:
            text: A string representing text to print in the echo area.
        """
        ihmacs_state = self.ihmacs_state
        text = ihmacs_state.echo

        window = ihmacs_state.window

        # Get dimensions of terminal
        term_lines, term_cols = ihmacs_state.term_size

        # Line to echo on, last line
        display_line = term_lines - 1

        # Get original location of cursor so we can return it
        cursor_pos = window.getyx()

        # Truncate the string if it is too long, adding indicator that it's
        # truncated.
        if len(text) > term_cols:
            text = text[:-3] + "..."

        window.addstr(display_line, 0, text)  # Echo at the bottom of the term
        window.clrtoeol()  # Clear any leftovers in echo area
        window.move(cursor_pos[0], cursor_pos[1])  # Restore cursor
