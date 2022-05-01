"""
Basic editing commands for Ihmacs.

All these functions can take custom arguments, but the first argument
must be an Ihmacs object containing the global state of the editor.
"""

from buff import Buffer

import curses


def self_insert_command(ihmacs_state):
    """
    Insert the character you type at point.

    Args:
        ihmacs_state: The entire global Ihmacs state as an Ihmacs instance.
    """
    buff = ihmacs_state.active_buff
    keychord = ihmacs_state.keychord
    # The last stroke typed in the keychord
    char = keychord[-1]
    buff.insert(char)


def insert(ihmacs_state, string):
    """
    Insert string at point in buffer.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        string: A string to insert into the buffer.
    """
    buff = ihmacs_state.active_buff
    buff.insert(string)


# TODO: Make find_file actually open a file
def find_file(ihmacs_state):
    """
    Find and open a file.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    insert(ihmacs_state,
           "This would open a file, had I implemented that yet")


def kill_ihmacs(ihmacs_state):
    """
    Kills the editor.

    WARNING: DOES NOT CHECK TO SAVE

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    ihmacs_state.end_session = True


# TODO: Make this actually display the error message
def command_undefined(ihmacs_state):
    """
    Tell user typed keychord is not mapped.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    pass


def delete_char(ihmacs_state, num=1):
    """
    Delete num characters at point.

    If num is positive, delete characters after point. If num is negative,
    delete characters before point.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: An integer representing how many characters to delete. The sign
            denotes the direction.
    """
    buff = ihmacs_state.active_buff

    buff.delete_char(num)


def backwards_delete_char(ihmacs_state, num=1):
    """
    Delete num characters at point.

    If num is negative, delete characters after point. If num is positive,
    delete characters before point.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: An integer representing how many characters to delete. The sign
            denotes the direction.
    """
    buff = ihmacs_state.active_buff

    buff.delete_char(-num)


def newline(ihmacs_state, num=1):
    """
    Insert N newlines at point.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: Number of lines to insert. Must be 1 or greater.
    """
    for i in range(num):
        insert(ihmacs_state, "\n")


def forward_char(ihmacs_state, num=1):
    """
    Move point forward N chars.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: Number of characters to move point. If negative, move point
            backwards.
    """
    buff = ihmacs_state.active_buff
    point = buff.point
    buff.set_point(point + num)


def backward_char(ihmacs_state, num=1):
    """
    Move point backward N chars.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: Number of characters to move point. If negative, move point
            forwards.
    """
    buff = ihmacs_state.active_buff
    point = buff.point
    buff.set_point(point - num)


def point_max(ihmacs_state):
    """
    Return the maximum allowed point of the active buffer.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    buff = ihmacs_state.active_buff
    text = buff.text
    return len(text)


# This function exists for if I were to add narrowing in the future.
def point_min(ihmacs_state):
    """
    Return the minimum allowed point of the active buffer.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    return 0


def move_end_of_line(ihmacs_state):
    """
    Move point to start of the current line.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    buff = ihmacs_state.active_buff
    point = buff.point
    text = buff.text
    end_of_text = point_max(ihmacs_state)

    while point < end_of_text:
        if text[point] == "\n":
            break
        point += 1
    buff.set_point(point)


def move_beginning_of_line(ihmacs_state):
    """
    Move point to start of the current line.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    buff = ihmacs_state.active_buff
    point = buff.point
    text = buff.text
    start_of_text = point_min(ihmacs_state)

    while point > start_of_text:
        if text[point-1] == "\n":
            break
        point -= 1
    buff.set_point(point)


def previous_line(ihmacs_state, num=1):
    """
    Move up one line.

    Attempts to keep column position between lines. If the previous line is
    shorter than the original column position of the point, go to the end of
    that line.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: An int representing the number of lines to move. If negative, move
            to the next line.

    """
    if num == 0:
        return
    if num < 0:
        next_line(ihmacs_state, num=-num)
        return

    buff = ihmacs_state.active_buff
    point = buff.point
    original_col = buff.column  # We try to preserve this

    # Move to end of previous line. Do this NUM times.
    for _ in range(num):
        move_beginning_of_line(ihmacs_state)
        backward_char(ihmacs_state)

    newline_col = buff.column  # Number of columns in the current line

    # Adjust point to be in the same column
    if original_col < newline_col:
        backward_char(ihmacs_state, newline_col-original_col)


def next_line(ihmacs_state, num=1):
    """
    Move down one line.

    Attempts to keep column position between lines. If the next line is shorter
    than the original column position of the point, go to the end of that line.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: An int representing the number of lines to move. If negative, move
            to the next line.

    """
    if num == 0:
        return
    if num < 0:
        previous_line(ihmacs_state, num=-num)
        return

    buff = ihmacs_state.active_buff
    point = buff.point
    original_col = buff.column  # We try to preserve this

    # Move to the start of next line. Do this NUM times.
    for _ in range(num):
        move_end_of_line(ihmacs_state)
        forward_char(ihmacs_state)

    # Move to end of line to find the total number of columns in the line.
    move_end_of_line(ihmacs_state)
    newline_col = buff.column  # Number of columns in the current line

    # Adjust point to be in the same column
    if original_col < newline_col:
        backward_char(ihmacs_state, newline_col-original_col)


def scroll_up(ihmacs_state, num=1):
    """
    Scroll buffer up N lines.

    By scroll up, it's as if the buffer was a piece of paper and you pushed up
    on it. Scrolling up will actually show you further down in the buffer.

    If point is moved out of the view, moves point accordingly.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: The number of lines to scroll. If negative, scroll down.
    """
    buff = ihmacs_state.active_buff
    buff.scroll_buffer(num)

    # Check that point is on a line within the view area
    view_min = buff.display_line
    view_max = view_min + curses.LINES - 2
    current_line = buff.line

    if current_line < view_min:
        next_line(ihmacs_state, view_min-current_line)
    if current_line >= view_max:
        previous_line(ihmacs_state, view_max-current_line+1)


def scroll_down(ihmacs_state, num=1):
    """
    Scroll buffer down N lines.

    By scroll down, it's as if the buffer was a piece of paper and you pushed
    down on it. Scrolling down will actually show you further up in the buffer.

    If point is moved out of the view, moves point accordingly.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: The number of lines to scroll. If negative, scroll down.
    """
    scroll_up(ihmacs_state, num=-num)
