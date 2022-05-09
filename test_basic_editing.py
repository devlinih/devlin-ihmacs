"""
Unit tests for editing commands.
"""


import pytest

from ihmacs_class import IhmacsSansCurses
from buff import Buffer

# Recycle this fantastic set of cases
from test_buff import (
    inital_buffer_states,
    LOREM_IPSUM,
)

# Reasonably testable functions, no curses/controller/view (any function that
# calls message and message itself), no random, etc.
from basic_editing import (
    self_insert_command,
    insert,
    set_mark_command,
    exchange_point_and_mark,
    create_buffer_no_switch,
    create_buffer,
    next_buffer,
    previous_buffer,
    kill_buffer,
    kill_ihmacs,
    newline,
    forward_char,
    backward_char,
    point_max,
    point_min,
    point_forward_by_delimiter,
    point_backward_by_delimiter,
    beginning_of_buffer,
    end_of_buffer,
    thing_at_point_regex,
    kill_append,
    kill_ring_save,
    kill_forward_by_delimiter,
    kill_backward_by_delimiter,
    kill_line,
    backward_kill_line,
    forward_kill_word,
    backward_kill_word,
)


@pytest.fixture(params=inital_buffer_states)
def buff(request):
    """
    Return a text buffer in some original state.
    """
    text = request.param[0]
    point = request.param[1]
    mark = request.param[2]

    buff = Buffer()

    # Directly set attributes, do not depend on methods for tests.
    buff._text = text
    buff._point = point
    buff._mark = mark
    return buff


kill_ring_states = [
    [],
    ["one kill."],
    ["once kill,", "two kills."],
]


@pytest.fixture(params=kill_ring_states)
def kill_ring(request):
    """
    Return a list of strings representing a kill ring.
    """
    return request.param


@pytest.fixture(params=range(3))
def ihmacs_state(request, buff, kill_ring):
    """
    Return an Ihmacs instance in some original state.

    The instance has N identical buffers.

    Args:
        buff: A buffer instance in some original state.
        kill_ring: A list of strings representing a kill ring.
    """
    num_buffers = request.param

    # The empty list would be argparse files
    ihmacs = IhmacsSansCurses([])
    ihmacs._buffers = [buff] * num_buffers
    ihmacs.kill_ring = kill_ring
    return ihmacs


keychords_alphanumeric = [
    ["`"], ["1"], ["2"], ["3"], ["4"], ["5"], ["6"], ["7"], ["8"], ["9"],
    ["0"], ["-"], ["="], ["~"], ["!"], ["@"], ["#"], ["$"], ["%"], ["^"],
    ["&"], ["*"], ["("], [")"], ["_"], ["+"], ["q"], ["w"], ["e"], ["r"],
    ["t"], ["y"], ["u"], ["i"], ["o"], ["p"], ["["], ["]"], ["\\"], ["Q"],
    ["W"], ["E"], ["R"], ["T"], ["Y"], ["U"], ["I"], ["O"], ["P"], ["{"],
    ["}"], ["|"], ["a"], ["s"], ["d"], ["f"], ["g"], ["h"], ["j"], ["k"],
    ["l"], [";"], ["'"], ["A"], ["S"], ["D"], ["F"], ["G"], ["H"], ["J"],
    ["K"], ["L"], [":"], ['"'], ["z"], ["x"], ["c"], ["v"], ["b"], ["n"],
    ["m"], [","], ["."], ["/"], ["Z"], ["X"], ["C"], ["V"], ["B"], ["N"],
    ["M"], ["<"], [">"], ["?"], [" "],
]


@pytest.fixture(params=keychords_alphanumeric)
def keychord(request):
    """
    Return a keychord that is simply an alphanumeric character.
    """
    return request.param


insert_strings = [
    "",
    "Hello, World!",
    "abc123",
    "New\nline",
    "qwerty",
    LOREM_IPSUM,
]


@pytest.fixture(params=insert_strings)
def insert_string(request):
    """
    Return a string to inset into a buffer.
    """
    return request.param


buffer_names = [
    "*messages*",
    "*scratch*",
    "*completions*",
    "init.el",
    "ihmacs.py",
    "test_basic_editing.py",
    "hello.c",
]


@pytest.fixture(params=buffer_names)
def buffer_name(request):
    """
    Return a string representing a buffer name.
    """
    return request.param


@pytest.fixture(params=range(5))
def times(request):
    """
    Return an integer representing how many times to repeat a command.
    """
    return request.param


# Let the testing begin

# self_insert_command
def test_self_insert_command(ihmacs_state, keychord):
    """
    Test that self_insert_command inserts the correct character at point.

    Checks that point has moved 1 forward, and the previous character is the
    last key in the keychord.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
        keychord: A list of strings representing a keychord.
    """
    og_buff = ihmacs_state.active_buff()
    og_point = og_buff.point
    inserted_char_keychord = keychord[-1]

    ihmacs_state.keychord = keychord
    self_insert_command(ihmacs_state)

    new_buff = ihmacs_state.active_buff()
    new_point = new_buff.point
    inserted_char_buff = new_buff.text[og_point]

    assert (inserted_char_keychord == inserted_char_buff
            and og_point == new_point-1)


# insert
def test_insert(ihmacs_state, insert_string):
    """
    Test that insert correctly inserts string at point.

    Checks that the segment of buffer text from the original point to the new
    point is the insert string.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
        insert_string: A string to insert into the buffer at point.
    """
    buff = ihmacs_state.active_buff()
    og_point = buff.point

    insert(ihmacs_state, insert_string)

    new_point = buff.point
    text = buff.text

    assert insert_string == text[og_point:new_point]


# set_mark_command
def test_set_mark_command(ihmacs_state):
    """
    Test that set_mark_command correctly sets mark to current point.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    og_buff = ihmacs_state.active_buff()
    og_point = og_buff.point

    set_mark_command(ihmacs_state)

    new_buff = ihmacs_state.active_buff()
    new_mark = new_buff.mark

    assert og_point == new_mark


# exchange_point_and_mark
def test_exchange_point_and_mark(ihmacs_state):
    """
    Test that exchange_point_and_mark correctly exchanges point and mark.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    og_buff = ihmacs_state.active_buff()
    og_point = og_buff.point
    og_mark = og_buff.mark

    exchange_point_and_mark(ihmacs_state)

    new_buff = ihmacs_state.active_buff()
    new_point = new_buff.point
    new_mark = new_buff.mark

    assert og_point == new_mark and og_mark == new_point


# create_buffer_no_switch
def test_create_buffer_no_switch(ihmacs_state, buffer_name):
    """
    Test that a new buffer is created but not switched to.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
        buffer_name: A string representing the name of the buffer to create.
    """
    og_buffer_index = ihmacs_state.active_buff_index
    og_buffer_count = len(ihmacs_state.buffers)

    create_buffer_no_switch(ihmacs_state, name=buffer_name)

    new_buffer_index = ihmacs_state.active_buff_index
    new_buffer_count = len(ihmacs_state.buffers)

    assert (og_buffer_index == new_buffer_index
            and og_buffer_count == new_buffer_count - 1)


# create_buffer
def test_create_buffer(ihmacs_state, buffer_name):
    """
    Test that a new buffer is created and switched to.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
        buffer_name: A string representing the name of the buffer to create.
    """
    og_buffer_index = ihmacs_state.active_buff_index
    og_buffer_count = len(ihmacs_state.buffers)

    create_buffer(ihmacs_state, name=buffer_name)

    new_buffer_index = ihmacs_state.active_buff_index
    new_buffer_count = len(ihmacs_state.buffers)

    assert (new_buffer_index == new_buffer_count - 1
            and og_buffer_count == new_buffer_count - 1)


# next_buffer
def test_next_buffer(ihmacs_state):
    """
    Test that the next buffer is properly cycled to.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    # Ensure there is an active buffer
    ihmacs_state.active_buff()

    og_buffer_index = ihmacs_state.active_buff_index
    buffer_count = len(ihmacs_state.buffers)

    if og_buffer_index == buffer_count - 1:
        expected_index = 0
    else:
        expected_index = og_buffer_index + 1

    next_buffer(ihmacs_state)

    new_buffer_index = ihmacs_state.active_buff_index

    assert expected_index == new_buffer_index


# previous_buffer
def test_prevous_buffer(ihmacs_state):
    """
    Test that the next buffer is properly cycled to.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    # Ensure there is an active buffer
    ihmacs_state.active_buff()

    og_buffer_index = ihmacs_state.active_buff_index
    buffer_count = len(ihmacs_state.buffers)

    if og_buffer_index == 0:
        expected_index = buffer_count - 1
    else:
        expected_index = og_buffer_index - 1

    previous_buffer(ihmacs_state)

    new_buffer_index = ihmacs_state.active_buff_index

    assert expected_index == new_buffer_index


# kill_buffer
def test_kill_buffer(ihmacs_state):
    """
    Test that the active buffer is killed.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    # Ensure there is an active buffer
    ihmacs_state.active_buff()

    og_buffer_list = ihmacs_state.buffers
    buffer_index = ihmacs_state.active_buff_index
    expected_buffer_list = (og_buffer_list[:buffer_index]
                            + og_buffer_list[buffer_index+1:])

    kill_buffer(ihmacs_state)

    new_buffer_list = ihmacs_state.buffers

    assert new_buffer_list == expected_buffer_list


# kill_ihmacs
def test_kill_ihmacs(ihmacs_state):
    """
    Test that end_session is correctly updated in a given editor state.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    kill_ihmacs(ihmacs_state)
    assert ihmacs_state.end_session


# newline
def test_newline(ihmacs_state, times):
    """
    Test that the correct number of newline characters are inserted.

    Args:
        ihmacs_state An instance of IhmacsSansCurses.
        times: An integer representing how many times to repeat a command.
    """
    buff = ihmacs_state.active_buff()
    og_point = buff.point
    expected_string = "\n" * times

    newline(ihmacs_state, num=times)

    new_point = buff.point
    assert expected_string == buff.text[og_point:new_point]


# forward_char
def test_forward_char(ihmacs_state, times):
    """
    Test that point is moved the correct number of characters forward.

    Args:
        ihmacs_state An instance of IhmacsSansCurses.
        times: An integer representing how many times to repeat a command.
    """
    buff = ihmacs_state.active_buff()
    og_point = buff.point
    expected_point = max(0, min(og_point+times, len(buff.text)))

    forward_char(ihmacs_state, num=times)

    new_point = buff.point
    assert expected_point == new_point


# backward_char
def test_backward_char(ihmacs_state, times):
    """
    Test that point is moved the correct number of characters backward.

    Args:
        ihmacs_state An instance of IhmacsSansCurses.
        times: An integer representing how many times to repeat a command.
    """
    buff = ihmacs_state.active_buff()
    og_point = buff.point
    expected_point = max(0, min(og_point-times, len(buff.text)))

    backward_char(ihmacs_state, num=times)

    new_point = buff.point
    assert expected_point == new_point


# point_max
def test_point_max(ihmacs_state):
    """
    Test that the correct max point is returned.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    buff = ihmacs_state.active_buff()
    expected_point = len(buff.text)
    assert expected_point == point_max(ihmacs_state)


# point_min
def test_point_min(ihmacs_state):
    """
    Test that the correct min point is returned.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    expected_point = 0
    assert expected_point == point_min(ihmacs_state)


# beginning_of_buffer
def test_beginning_of_buffer(ihmacs_state):
    """
    Test that point is correctly set to beginning of buffer.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    beginning_of_buffer(ihmacs_state)
    buff = ihmacs_state.active_buff()
    assert 0 == buff.point


# end_of_buffer
def test_end_of_buffer(ihmacs_state):
    """
    Test that point is correctly set to end of buffer.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    end_of_buffer(ihmacs_state)
    buff = ihmacs_state.active_buff()
    expected_point = len(buff.text)
    assert expected_point == buff.point


# kill_append
def test_kill_append(ihmacs_state, insert_string):
    """
    Test that text is correctly inserted into kill_ring.

    Note, kill_append does not insert the empty string into the kill ring, so
    have an if statement to check that.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
        insert_string: A string to append to the killring.
    """
    if insert_string == "":
        pytest.skip("kill_append does not insert empty string.")
    kill_append(ihmacs_state, insert_string)
    assert insert_string == ihmacs_state.kill_ring[-1]


# kill_ring_save
def test_kill_ring_save(ihmacs_state):
    """
    Test that region is correctly appended to kill ring.

    Note, kill_append does not insert the empty string into the kill ring, so
    have an if statement to check that.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    buff = ihmacs_state.active_buff()
    text = buff.text
    points = (buff.point, buff.mark)
    start = min(points)
    end = max(points)
    expected_kill = text[start:end]

    if expected_kill == "":
        pytest.skip("kill_append (called by kill_ring_save) "
                    "does not insert empty string.")
    kill_ring_save(ihmacs_state)
    assert expected_kill == ihmacs_state.kill_ring[-1]


# kill_forward_by_delimiter

# kill_backward_by_delimiter

# kill_line

# backward_kill_line

# forward_kill_word

# backward_kill_word
