"""
Unit tests for Ihmacs class.

The helper function `read_keychord_keymap`---despite having no side effects and
only depending on arguments, not state---is not tested because it deals with
higher order functions, and Python's handling of higher order function equality
is unpredictable.
"""

import pytest

from ihmacs_class import IhmacsSansCurses
from buff import Buffer


# (num_buffs, active_buff)
initial_ihmacs_state = [(0, 0),
                        (1, 0),
                        (2, 0),
                        (3, 0),
                        (4, 0),
                        (5, 0),
                        (2, 1),
                        (3, 1),
                        (4, 1),
                        (5, 1),
                        (3, 2),
                        (4, 2),
                        (5, 2),
                        (4, 3),
                        (5, 3),
                        (5, 4),
                        # Invalid indexes
                        (1, 3),
                        (2, 3),
                        (3, 5)]


@pytest.fixture(params=initial_ihmacs_state)
def ihmacs_state(request):
    """
    Return an instance of the Ihmacs class (sans curses) with N buffers.
    """
    num_buffs = request.param[0]
    active_buff = request.param[1]
    # The empty list would be argparse files.
    ihmacs = IhmacsSansCurses([])
    buffers = [Buffer(name=str(i)) for i in range(num_buffs)]
    ihmacs._buffers = buffers
    ihmacs._active_buff = active_buff
    return ihmacs


index_cases = range(-3, 9)


@pytest.fixture(params=index_cases)
def index(request):
    """
    Return an integer representing a buffer index.
    """
    return request.param


name_cases = ["-1",
              "0",
              "1",
              "2",
              "3",
              "4",
              "5",
              "6",
              "7",
              "foobar",
              "*scratch*", ]


@pytest.fixture(params=name_cases)
def name(request):
    """
    Return a string representing a buffer name.
    """
    return request.param


# active buff property
def test_active_buff_return(ihmacs_state):
    """
    Test that active_buff always returns a buffer.

    This should always return a buffer, fixing the index if it's invalid and
    creating a new buffer if there are none.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    buff = ihmacs_state.active_buff
    assert isinstance(buff, Buffer)


# create_buffer_no_switch
def test_create_buffer_no_switch(ihmacs_state):
    """
    Test that a buffer is created but not switched to.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    num_buffers = len(ihmacs_state.buffers)
    buff_index = ihmacs_state.active_buff_index

    ihmacs_state.create_buffer_no_switch()

    new_num_buffers = len(ihmacs_state.buffers)
    new_buff_index = ihmacs_state.active_buff_index

    assert num_buffers == new_num_buffers - 1 and buff_index == new_buff_index


# create_buffer
def test_create_buffer(ihmacs_state):
    """
    Test that a buffer is created and switched to.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
    """
    num_buffers = len(ihmacs_state.buffers)

    ihmacs_state.create_buffer()

    new_num_buffers = len(ihmacs_state.buffers)
    new_buff_index = ihmacs_state.active_buff_index

    assert (num_buffers == new_num_buffers - 1
            and new_buff_index == new_num_buffers - 1)


# switch_buffer
def test_switch_buffer(ihmacs_state, index):
    """
    Test that the correct buffer is switched too.

    If the index falls out of range of the buffer list, nothing should happen.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
        index: An integer representing a buffer index.
    """
    og_buffer_index = ihmacs_state.active_buff_index
    num_buffers = len(ihmacs_state.buffers)

    ihmacs_state.switch_buffer(index)

    # Check if index was invalid
    if 0 <= index < num_buffers:  # Valid
        assert index == ihmacs_state.active_buff_index
    else:  # Invalid index
        assert og_buffer_index == ihmacs_state.active_buff_index


# kill_buffer
def test_kill_buffer(ihmacs_state, index):
    """
    Test that the correct buffer is killed.

    If the index falls out of range of the buffer list, nothing should happen.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
        index: An integer representing a buffer index.
    """
    num_buffers = len(ihmacs_state.buffers)

    ihmacs_state.kill_buffer(index)

    # Check if index was invalid
    if 0 <= index < num_buffers:  # Valid
        new_num_buffers = len(ihmacs_state.buffers)
        assert num_buffers == new_num_buffers + 1
    else:  # Invalid index
        new_num_buffers = len(ihmacs_state.buffers)
        assert num_buffers == new_num_buffers


# find_buffer
def test_find_buffer(ihmacs_state, name):
    """
    Test that the correct buffer is found, or None if there is no match.

    Args:
        ihmacs_state: An instance of IhmacsSansCurses.
        name: A string representing a buffer name to search for.
    """
    buffers = ihmacs_state.buffers
    found_buffer = None
    for i in buffers:
        if i.name == name:
            found_buffer = i
            break
    assert found_buffer == ihmacs_state.find_buffer(name)
