"""
Basic editing commands for Ihmacs.

All these functions can take custom arguments, but the first argument
must be an Ihmacs object containing the global state of the editor.
"""

import re
from string import (
    ascii_letters,
    digits,
    punctuation,
)
from random import randrange

from tree_helpers import build_tree_from_pairs


def self_insert_command(ihmacs_state):
    """
    Insert the character you type at point.

    Args:
        ihmacs_state: The entire global Ihmacs state as an Ihmacs instance.

    Returns:
        A string representing the inserted text. If the buffer is read only,
        this is the empty string.
    """
    buff = ihmacs_state.active_buff
    keychord = ihmacs_state.keychord
    # The last stroke typed in the keychord
    char = keychord[-1]

    # Side effects
    return insert(ihmacs_state, char)


def insert(ihmacs_state, string):
    """
    Insert string at point in buffer.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        string: A string to insert into the buffer.

    Returns:
        A string representing the inserted text. If the buffer is read only,
        this is the empty string.
    """
    buff = ihmacs_state.active_buff

    # Side effects
    inserted_text = buff.insert(string)

    # Read only check
    if inserted_text == False:
        message(ihmacs_state, f"{buff.name} is read only.")
        return ""
    return inserted_text


def set_mark_command(ihmacs_state):
    """
    Set the mark to location of current point.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    buff = ihmacs_state.active_buff
    point = buff.point
    buff.set_mark(point)


def exchange_point_and_mark(ihmacs_state):
    """
    Swap the locations of point and mark.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    buff = ihmacs_state.active_buff
    point = buff.point
    mark = buff.mark
    buff.set_point(mark)
    buff.set_mark(point)


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


def create_buffer(ihmacs_state, name=None):
    """
    Create a new buffer and switch to it.

    If a name is not specified, give the buffer a random name. This random name
    is just a random 6 digit integer.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    if name is None:
        name = "*"+str(randrange(100000, 999999))+"*"

    ihmacs_state.create_buffer(name=name)


def next_buffer(ihmacs_state):
    """
    Switch to the next buffer in the buffer list.

    If the active buffer is the last buffer, switch to the first buffer.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    buffer_list = ihmacs_state.buffers
    current_buff_index = ihmacs_state.active_buff_index
    next_buff_index = current_buff_index + 1
    if len(buffer_list) == next_buff_index:
        next_buff_index = 0

    ihmacs_state.switch_buffer(next_buff_index)


def previous_buffer(ihmacs_state):
    """
    Switch to the previous buffer in the buffer list.

    If the active buffer is the first buffer, switch to the last buffer.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    buffer_list = ihmacs_state.buffers
    current_buff_index = ihmacs_state.active_buff_index
    next_buff_index = current_buff_index - 1
    if next_buff_index < 0:
        next_buff_index = len(buffer_list) - 1

    ihmacs_state.switch_buffer(next_buff_index)


def kill_buffer(ihmacs_state):
    """
    Kill the active buffer.

    There is no going back after executing this command. The buffer is gone.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    active_buff_index = ihmacs_state.active_buff_index
    ihmacs_state.kill_buffer(active_buff_index)


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

    Returns:
        A string representing the deleted text.
    """
    buff = ihmacs_state.active_buff

    # Side effects
    deleted_text = buff.delete_char(num)

    # Read only check
    if deleted_text == False:
        message(ihmacs_state, f"{buff.name} is read only.")
        return ""
    return deleted_text


def backwards_delete_char(ihmacs_state, num=1):
    """
    Delete num characters at point.

    If num is negative, delete characters after point. If num is positive,
    delete characters before point.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: An integer representing how many characters to delete. The sign
            denotes the direction.

    Returns:
        A string representing the deleted text.
    """
    buff = ihmacs_state.active_buff

    # Side effects
    return delete_char(ihmacs_state, num=-num)


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


def point_forward_by_delimiter(ihmacs_state, delimiter_regex, num=1):
    """
    Return the point at the location forward N units separated by a delimiter.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        delimiter_regex: A compiled regex that searches for instances of the
            delimiter.
        num: The number of units to search forward.

    Returns:
        An int representing the location of the point moved forward by N
        delimiter separated units.
    """
    if num == 0:
        return 0
    if num < 0:
        return point_backward_by_delimiter(ihmacs_state,
                                           delimiter_regex,
                                           num=-num)

    buff = ihmacs_state.active_buff
    text = buff.text
    point = buff.point

    delimiters = delimiter_regex.finditer(text)
    # Units end at the start of delimiters. Find all ends after point.
    unit_ends = [i.start() for i in delimiters if i.start() > point]

    try:
        # Find the end of the nth next unit
        new_point = unit_ends[num-1]
        return new_point
    except IndexError:
        # If we are trying to go too far ahead, that means we are in the
        # last unit already. Move to the end of it.
        new_point = point_max(ihmacs_state)
        return new_point


def point_backward_by_delimiter(ihmacs_state, delimiter_regex, num=1):
    """
    Return the point at the location backward N units separated by a delimiter.

    Args:
        Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        delimiter_regex: A compiled regex that searches for instances of the
            delimiter.
        num: The number of units to search forward.

    Returns:
        An int representing the location of the point moved backward by N
        delimiter separated unit.
    """
    if num == 0:
        return 0
    if num < 0:
        return point_forward_by_delimiter(ihmacs_state,
                                          delimiter_regex,
                                          num=-num)

    buff = ihmacs_state.active_buff
    text = buff.text
    point = buff.point

    delimiters = delimiter_regex.finditer(text)
    # Units start at the end of delimiters. Find all starts before point.
    unit_starts = [i.end() for i in delimiters if i.end() < point]

    try:
        # Find the start of the nth previous unit
        new_point = unit_starts[-num]
        return new_point
    except IndexError:
        # If we are trying to go too far back, that means go to the
        # first unit, or just the start of the buffer.
        new_point = point_min(ihmacs_state)
        return new_point


def forward_by_delimiter(ihmacs_state, delimiter_regex, num=1):
    """
    Move point forward by N units separated by a delimiter.

    This command is used to define other commands such as forward_word.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        delimiter_regex: A compiled regex that searches for instances of the
            delimiter.
        num: The number of units to move forward.
    """
    buff = ihmacs_state.active_buff
    new_point = point_forward_by_delimiter(ihmacs_state,
                                           delimiter_regex,
                                           num=num)
    buff.set_point(new_point)


def backward_by_delimiter(ihmacs_state, delimiter_regex, num=1):
    """
    Move point backward by N units separated by a delimiter.

    This command is used to define the behavior of forward_by_delimiter with a
    negative argument.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        delimiter_regex: A compiled regex that searches for instances of the
            delimiter.
        num: The number of units to move backward.
    """
    buff = ihmacs_state.active_buff
    new_point = point_backward_by_delimiter(ihmacs_state,
                                            delimiter_regex,
                                            num=num)
    buff.set_point(new_point)


def forward_word(ihmacs_state, num=1):
    """
    Move point forward N words.

    Places point at the end of a word.

    A word is defined as being delimited by the mode specific word delimiters.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: The number of words to move forward. If negative, move backwards.
    """
    buff = ihmacs_state.active_buff
    major_mode = buff.major_mode
    delimiter_regex = major_mode.word_delimiters_regex
    forward_by_delimiter(ihmacs_state, delimiter_regex, num=num)


def backward_word(ihmacs_state, num=1):
    """
    Move point backward N words.

    Places point at the start of a word.

    A word is defined as being delimited by the mode specific word delimiters.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: The number of words to move backward. If negative, move forwards.
    """
    forward_word(ihmacs_state, num=-num)


def move_end_of_line(ihmacs_state):
    """
    Move point to start of the current line.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    # Test if we are already at the end of a line
    buff = ihmacs_state.active_buff
    text = buff.text
    point = buff.point
    try:
        current_char = text[point]
    except IndexError:
        # End of File
        current_char = "\n"
    if current_char == "\n":
        # We are already at the end of a line.
        return

    newline = "\n+"
    newline_regex = re.compile(newline)
    forward_by_delimiter(ihmacs_state, newline_regex)


def move_beginning_of_line(ihmacs_state):
    """
    Move point to start of the current line.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    # Test if we are already at the start of a line
    buff = ihmacs_state.active_buff
    column = buff.column
    if column == 0:
        return

    newline = "\n+"
    newline_regex = re.compile(newline)
    backward_by_delimiter(ihmacs_state, newline_regex)


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

    # Remember original column
    buff = ihmacs_state.active_buff
    original_column = buff.column

    for _ in range(num):
        move_beginning_of_line(ihmacs_state)
        backward_char(ihmacs_state)

    # Adjust column
    new_column = buff.column
    adjust_chars = max(0, new_column-original_column)
    backward_char(ihmacs_state, adjust_chars)


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

    # Remember original column
    buff = ihmacs_state.active_buff
    original_column = buff.column

    for _ in range(num):
        move_end_of_line(ihmacs_state)
        forward_char(ihmacs_state)

    # Adjust column
    current_line = line_at_point(ihmacs_state)
    current_line_len = len(current_line)
    adjust_chars = min(original_column, current_line_len)
    forward_char(ihmacs_state, adjust_chars)


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


# This does not do what the actual thing-at-point function does in GNU/Emacs,
# although it could be used as a helper function do so (or maybe
# not). Regardless, that doesn't matter.
def thing_at_point_regex(ihmacs_state, thing_regex):
    """
    Return the thing the point is located in that is defined by a regex.

    The buffer is a string. The buffer is split into units, which are defined
    by a regex. The thing at point is the unit which the point is located
    within.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        thing_regex: A compiled regex defining the unit delimiters.

    Returns:
        A string representing the thing at point. If point is not at a unit,
        return the empty string.
    """
    buff = ihmacs_state.active_buff
    text = buff.text
    point = buff.point

    units = thing_regex.finditer(text)
    for unit in units:
        start, end = unit.span()
        if start <= point <= end:
            return text[start:end]
    # Point is not at a unit
    return ""


def line_at_point(ihmacs_state):
    """
    Return the line at point.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.

    Returns:
        A string representing the contents of the current line.
    """
    line_regex_string = "^.*$"
    line_regex = re.compile(line_regex_string,
                            re.MULTILINE)
    return thing_at_point_regex(ihmacs_state, line_regex)


def word_at_point(ihmacs_state):
    """
    Return the word at point.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.

    Returns:
        A string representing the word at which the point is located in.
    """
    buff = ihmacs_state.active_buff
    major_mode = buff.major_mode
    word_regex = major_mode.word_regex

    return thing_at_point_regex(ihmacs_state, word_regex)


def kill_append(ihmacs_state, text):
    """
    Append text to kill_ring.

    If text is the empty string, does nothing.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        text: A string representing text to add to the kill ring.
    """
    if text == "":
        return

    kill_ring = ihmacs_state.kill_ring
    kill_ring.append(text)


def yank(ihmacs_state, kill=1):
    """
    Insert the nth most recent kill into the buffer at point.

    If kill_ring is empty, print a message.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        kill: An int representing N in the Nth most recent kill.
    """
    kill_ring = ihmacs_state.kill_ring
    if kill_ring == []:
        message(ihmacs_state, "kill_ring is empty.")
        return

    if kill > len(kill_ring):
        kill = 1

    kill_text = kill_ring[-kill]

    insert(ihmacs_state, kill_text)


def kill_region(ihmacs_state):
    """
    Kill text in region and append to kill ring.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    buff = ihmacs_state.active_buff
    kill_text = buff.delete_region()

    # Read only check
    if deleted_text == False:
        message(ihmacs_state, f"{buff.name} is read only.")
        return

    kill_append(ihmacs_state, kill_text)


def kill_ring_save(ihmacs_state):
    """
    Save region to kill ring, but do not kill it.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
    """
    buff = ihmacs_state.active_buff
    text = buff.text
    point = buff.point
    mark = buff.mark

    kill_text = text[point:mark]
    kill_append(ihmacs_state, kill_text)


def kill_forward_by_delimiter(ihmacs_state, delimiter_regex, num=1):
    """
    Kill forwards N units of text separated by a delimiter.

    Like forward_by_delimiter, but it kills the text.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        delimiter_regex: A compiled regex that searches for instances of the
            delimiter.
        num: The number of units to kill
    """
    buff = ihmacs_state.active_buff
    point = buff.point

    kill_point = point_forward_by_delimiter(ihmacs_state,
                                            delimiter_regex,
                                            num=num)
    # Side effects
    chars_to_delete = kill_point - point
    killed_text = delete_char(ihmacs_state, num=chars_to_delete)
    kill_append(ihmacs_state, killed_text)


def kill_backward_by_delimiter(ihmacs_state, delimiter_regex, num=1):
    """
    Kill backwards N units of text separated by a delimiter.

    Like backward_by_delimiter, but it kills the text.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        delimiter_regex: A compiled regex that searches for instances of the
            delimiter.
        num: The number of units to kill
    """
    kill_forward_by_delimiter(ihmacs_state, delimiter_regex, num=-num)


def kill_line(ihmacs_state, num=1):
    """
    Kill the rest of the current line after point.

    Adds killed text to kill_ring.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: An integer representing the number of lines to kill.
    """
    newline = "\n+"
    newline_regex = re.compile(newline)
    kill_forward_by_delimiter(ihmacs_state, newline_regex, num=num)


def backward_kill_line(ihmacs_state, num=1):
    """
    Kill the current line before point.

    Adds killed text to kill_ring.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: An integer representing the number of lines to kill.
    """
    kill_line(ihmacs_state, num=-num)


def forward_kill_word(ihmacs_state, num=1):
    """
    Delete up to end of word at point.

    Does not delete characters in the word before point.

    Adds killed text to kill_ring.

    Unfortunately, unlike GNU/Emacs, running this command repeatedly creates
    a new entry in the kill ring each time instead of concatenating the
    consecutive killed words together.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: An integer representing the number of words to kill.
    """
    buff = ihmacs_state.active_buff
    major_mode = buff.major_mode
    delimiter_regex = major_mode.word_delimiters_regex
    kill_forward_by_delimiter(ihmacs_state, delimiter_regex, num=num)


def backward_kill_word(ihmacs_state, num=1):
    """
    Delete up to start of word at point.

    Does not delete characters in the word after point.

    Adds killed text to kill_ring.

    Unfortunately, unlike GNU/Emacs, running this command repeatedly creates
    a new entry in the kill ring each time instead of concatenating the
    consecutive killed words together.

    Args:
        ihmacs_state: The global state of the editor as an Ihmacs instance.
        num: An integer representing the number of words to kill.
    """
    forward_kill_word(ihmacs_state, num=-num)


# The default global keymap.
DEFAULT_GLOBAL_KEYMAP = build_tree_from_pairs(
    [[[i], self_insert_command]
     for i in ascii_letters+digits+punctuation+" "] +
    [[["C-j"], newline],  # Enter
     [["DEL"], backwards_delete_char],  # Backspace
     [["KEY_DC"], delete_char],  # Delete
     [["C-d"], delete_char],
     [["C-f"], forward_char],
     [["KEY_RIGHT"], forward_char],
     [["M-f"], forward_word],
     [["C-b"], backward_char],
     [["KEY_LEFT"], backward_char],
     [["M-b"], backward_word],
     [["C-n"], next_line],
     [["KEY_DOWN"], next_line],
     [["C-p"], previous_line],
     [["KEY_UP"], previous_line],
     [["C-a"], move_beginning_of_line],
     [["KEY_HOME"], move_beginning_of_line],
     [["C-e"], move_end_of_line],
     [["KEY_END"], move_end_of_line],
     [["C-v"], scroll_up],
     [["KEY_NPAGE"], scroll_up],
     [["M-v"], scroll_down],
     [["KEY_PPAGE"], scroll_down],
     [["C-k"], kill_line],
     [["C-y"], yank],
     [["C- "], set_mark_command],
     [["C-x", "C-x"], exchange_point_and_mark],
     [["C-w"], kill_region],
     [["M-w"], kill_ring_save],
     [["M-DEL"], backward_kill_word],
     [["M-d"], forward_kill_word],
     # Extended commands
     [["C-x", "C-f"], create_buffer],  # Real Emacs runs find-file
     [["C-x", "b"], next_buffer],  # Real Emacs runs switch-to-buffer
     [["C-x", "C-b"], previous_buffer],  # Real Emacs runs list-buffers
     [["C-x", "k"], kill_buffer],
     [["C-x", "C-c"], kill_ihmacs], ]
)
