"""
Basic editing commands for Ihmacs.

All these functions can take custom arguments, but the first argument
must be an Ihmacs object containing the global state of the editor.
"""

from string import (
    ascii_letters,
    digits,
    punctuation,
)


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


def message(ihmacs_state, string):
    """
    Print string in echo area and append to *messages* buffer.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        string: A message to send.
    """
    # TODO: Append to *messages*. Will do after multiple buffers and
    # switching has been implemented.

    # Echo
    controller = ihmacs_state.controller
    controller.echo(string)


# TODO: Make find_file actually open a file
def find_file(ihmacs_state):
    """
    Find and open a file.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    message(ihmacs_state,
            "This would open a file, had I implemented that.")


def kill_ihmacs(ihmacs_state):
    """
    Kills the editor.

    WARNING: DOES NOT CHECK TO SAVE

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    ihmacs_state.end_session = True


def command_undefined(ihmacs_state):
    """
    Tell user typed keychord is not mapped.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    keychord = ihmacs_state.keychord
    keychord_string = " ".join(keychord)
    error_message = f"{keychord_string} is undefined"
    message(ihmacs_state, error_message)


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
    for _ in range(num):
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


# Should rewrite with regex
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


# Should rewrite with regex
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


# Should rewrite with regex
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
    original_col = buff.column  # We try to preserve this

    # Move to end of previous line. Do this NUM times.
    for _ in range(num):
        move_beginning_of_line(ihmacs_state)
        backward_char(ihmacs_state)

    newline_col = buff.column  # Number of columns in the current line

    # Adjust point to be in the same column
    if original_col < newline_col:
        backward_char(ihmacs_state, newline_col-original_col)


# Should rewrite with regex
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

    # Get terminal size
    term_lines, _ = ihmacs_state.term_size

    # Check that point is on a line within the view area
    view_min = buff.display_line
    view_max = view_min + term_lines - 2
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


def forward_word(ihmacs_state, num=1):
    """
    Move point forward N words.

    Places point at the end of a word.

    A word is defined as being delimited by the mode specific word delimiters.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: The number of words to move forward. If negative, move backwards.
    """
    if num == 0:
        return
    if num < 0:
        backward_word(ihmacs_state, num=-num)
        return

    buff = ihmacs_state.active_buff
    word_delimiters = buff.major_mode.word_delimiters_regex
    text = buff.text
    point = buff.point

    delimiters = word_delimiters.finditer(text)
    # Words end at the start of delimiters. Find all after point.
    word_ends = [i.start() for i in delimiters if i.start() > point]

    try:
        # Find the end of the nth next word
        new_point = word_ends[num-1]
    except IndexError:
        # If we are trying to go too far ahead, that means go to the
        # last word, or just the end of the buffer.
        new_point = point_max(ihmacs_state)
    buff.set_point(new_point)


def backward_word(ihmacs_state, num=1):
    """
    Move point backward N words.

    Places point at the start of a word.

    A word is defined as being delimited by the mode specific word delimiters.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: The number of words to move backward. If negative, move forwards.
    """
    if num == 0:
        return
    if num < 0:
        forward_word(ihmacs_state, num=-num)
        return

    buff = ihmacs_state.active_buff
    word_delimiters = buff.major_mode.word_delimiters_regex
    text = buff.text
    point = buff.point

    delimiters = word_delimiters.finditer(text)
    # Words start at the end of delimiters. Find all before point.
    word_starts = [i.end() for i in delimiters if i.end() < point]

    try:
        # Find the start of the nth previous word
        new_point = word_starts[-num]
    except IndexError:
        # If we are trying to go too far back, that means go to the
        # first word, or just the start of the buffer.
        new_point = point_min(ihmacs_state)
    buff.set_point(new_point)


# The default global keymap.
DEFAULT_GLOBAL_KEYMAP = (
    {i: self_insert_command
     for i in ascii_letters+digits+punctuation+" "} |
    {"C-j": newline,
     "DEL": backwards_delete_char,
     "C-f": forward_char,
     "KEY_RIGHT": forward_char,
     "M-f": forward_word,
     "C-b": backward_char,
     "KEY_LEFT": backward_char,
     "M-b": backward_word,
     "C-n": next_line,
     "KEY_DOWN": next_line,
     "C-p": previous_line,
     "KEY_UP": previous_line,
     "C-a": move_beginning_of_line,
     "C-e": move_end_of_line,
     "C-v": scroll_up,
     "KEY_NPAGE": scroll_up,
     "M-v": scroll_down,
     "KEY_PPAGE": scroll_down,
     # Extended commands
     "C-x": {"C-f": find_file,
             "C-c": kill_ihmacs, }, }
)
