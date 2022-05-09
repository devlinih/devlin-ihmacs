"""
Unit tests for Buffer class.

Does not test the file IO methods as they are 1: hard to test, 2: not currently
being used by the project.
"""

import pytest

from buff import Buffer


# ("text", point, mark), these cases have the point and mark set at
# beginning, mid, and end
inital_buffer_states = [("Hello, World!", 0, 0),
                        ("Hello, World!", 6, 0),
                        ("Hello, World!", 13, 0),
                        ("Hello, World!", 0, 6),
                        ("Hello, World!", 6, 6),
                        ("Hello, World!", 13, 6),
                        ("Hello, World!", 0, 13),
                        ("Hello, World!", 6, 13),
                        ("Hello, World!", 13, 13), ]


@pytest.fixture(params=inital_buffer_states)
def buff(request):
    """
    Return a test buffer in some original state.
    """
    text = request.param[0]
    point = request.param[1]
    mark = request.param[2]

    buff = Buffer()

    # Directly set attributes, do not depend on methods that I am testing.
    buff._text = text
    buff._point = point
    buff._mark = mark
    return buff


@pytest.fixture(params=inital_buffer_states)
def buff_read_only(request):
    """
    Return a read only test buffer in some original state.
    """
    text = request.param[0]
    point = request.param[1]
    mark = request.param[2]

    buff = Buffer(read_only=True)

    # Directly set attributes, do not depend on methods that I am testing.
    buff._text = text
    buff._point = point
    buff._mark = mark
    return buff


insert_string_params = ["",
                        " ",
                        "a",
                        "1",
                        "Hello",
                        "Hello, World!",
                        "This\nis\na\nstring.",
                        "`1234567890-=~!@#$%^&*()_+",
                        "qwertyuiop[]\\QWERTYUIOP{}|",
                        "asdfghjkl;'ASDFGHJKL:\"",
                        "zxcvbnm,./ZXCVBNM<>?", ]


@pytest.fixture(params=insert_string_params)
def insert_string(request):
    """
    Create a string to insert into a buffer.
    """
    return request.param


chars_params = range(-30, 31)


@pytest.fixture(params=chars_params)
def chars(request):
    """
    Return an integer representing a number of chars to operate on.
    """
    return request.param


# Test Editing Methods

# insert
def test_insert_text(buff, insert_string):
    """
    Check that text is correctly inserted into the buffer.

    Args:
        buff: An Ihmacs buffer.
        insert_string: A string to insert into the buffer.
    """
    point = buff.point
    text_before_point = buff.text[0:point]
    text_after_point = buff.text[point:]

    buff.insert(insert_string)
    assert buff.text == text_before_point+insert_string+text_after_point


def test_insert_point(buff, insert_string):
    """
    Check that point is placed at the end of the inserted text.

    Args:
        buff: An Ihmacs buffer.
        insert_string: A string to insert into the buffer.
    """
    og_point = buff.point

    buff.insert(insert_string)
    assert buff.point == og_point + len(insert_string)


def test_insert_mark(buff, insert_string):
    """
    Check that mark is moved accordingly after insert.

    If the mark is located at point or before point, it should not move. If it
    is located after point, it should be moved the length of the insert string.

    Args:
        buff: An Ihmacs buffer.
        insert_string: A string to insert into the buffer.
    """
    og_mark = buff.mark
    og_point = buff.point

    buff.insert(insert_string)

    new_mark = buff.mark

    if og_mark > og_point:
        assert og_mark + len(insert_string) == new_mark
    else:
        assert og_mark == new_mark


def test_insert_modified(buff, insert_string):
    """
    Check that modified state of buffer is True after inserting text.

    Args:
        buff: An Ihmacs buffer.
        insert_string: A string to insert into the buffer.
    """
    buff.insert(insert_string)
    assert buff.modified


def test_insert_text_read_only(buff_read_only, insert_string):
    """
    Check that text is not inserted into a read only buffer.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
        insert_string: A string to attempt insert into the buffer.
    """
    text_og = buff_read_only.text
    buff_read_only.insert(insert_string)
    text_new = buff_read_only.text
    assert text_og == text_new


def test_insert_point_read_only(buff_read_only, insert_string):
    """
    Check that point does not move when inserting to a read only buffer.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
        insert_string: A string to attempt insert into the buffer.
    """
    og_point = buff_read_only.point
    buff_read_only.insert(insert_string)
    new_point = buff_read_only.point
    assert og_point == new_point


def test_insert_mark_read_only(buff_read_only, insert_string):
    """
    Check that mark is not moved when inserting into a read only buffer.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
        insert_string: A string to attempt insert into the buffer.
    """
    og_mark = buff_read_only.mark
    buff_read_only.insert(insert_string)
    new_mark = buff_read_only.mark
    assert og_mark == new_mark


def test_insert_modified_read_only(buff_read_only, insert_string):
    """
    Check that modified state of read only buffer is False.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
        insert_string: A string to attempt insert into the buffer.
    """
    buff_read_only.insert(insert_string)
    assert not buff_read_only.modified


# delete_char
def test_delete_char_text(buff, chars):
    """
    Check that text is correctly deleted from buffer.

    Args:
        buff: An Ihmacs buffer.
        chars: An integer representing the number of chars to delete.
    """
    og_text = buff.text

    points = (buff.point, max(0, min(len(og_text), buff.point+chars)))
    start = min(points)
    end = max(points)

    expected_text = og_text[:start] + og_text[end:]

    # Do the delete
    buff.delete_char(chars)
    assert buff.text == expected_text


def test_delete_char_point(buff, chars):
    """
    Check that point is moved accordingly after delete.

    If chars is positive or 0, point should not move. If chars is negative, point
    should be equal to 0 or og_point+chars, whichever is greater.

    Args:
        buff: An Ihmacs buffer.
        chars: An integer representing the number of chars to delete.
    """
    og_point = buff.point

    if chars < 0:
        expected_point = max(0, og_point+chars)
    else:
        expected_point = og_point

    # Do the delete
    buff.delete_char(chars)
    assert buff.point == expected_point


def test_delete_char_mark(buff, chars):
    """
    Check that mark is moved accordingly after deletion.

    If the mark is located after point, the mark should be moved the number of
    characters deleted to the left, or to the new location of point, whichever
    is greater.

    If the mark is before point, it should stay in the same place or be moved
    to the new location of point, whichever is less.

    If the mark is located at point, then its new position should be the same
    position as the new point.

    Args:
        buff: An Ihmacs buffer.
        chars: An integer representing the number of chars to delete.
    """
    og_mark = buff.mark
    og_point = buff.point

    deleted = len(buff.delete_char(chars))

    new_mark = buff.mark
    new_point = buff.point

    if og_mark > og_point:
        expected_mark = max(new_point, og_mark-deleted)
    elif og_mark < og_point:
        expected_mark = min(new_point, og_mark)
    else:
        expected_mark = new_point

    assert new_mark == expected_mark


def test_delete_char_modified(buff, chars):
    """
    Check that modified state of buffer is True after deleting text.

    Args:
        buff: An Ihmacs buffer.
        chars: An integer representing the number of chars to delete.
    """
    buff.delete_char(chars)
    assert buff.modified


def test_delete_char_return(buff, chars):
    """
    Check that the return value of method is equal to the delete string.

    Args:
        buff: An Ihmacs buffer.
        chars: An integer representing the number of chars to delete.
    """
    og_text = buff.text
    point = buff.point

    points = (point, max(0, min(len(og_text), point+chars)))
    start = min(points)
    end = max(points)

    delete_string = og_text[start:end]

    assert delete_string == buff.delete_char(chars)


def test_delete_char_text_read_only(buff_read_only, chars):
    """
    Check that nothing is deleted from a read only buffer.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
        chars: An integer representing the number of chars to delete.
    """
    text_og = buff_read_only.text
    buff_read_only.delete_char(chars)
    text_new = buff_read_only.text
    assert text_og == text_new


def test_delete_char_point_read_only(buff_read_only, chars):
    """
    Check that point does not move when deleting from a read only buffer.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
        chars: An integer representing the number of chars to delete.
    """
    og_point = buff_read_only.point
    buff_read_only.delete_char(chars)
    new_point = buff_read_only.point
    assert og_point == new_point


def test_delete_char_mark_read_only(buff_read_only, chars):
    """
    Check that mark is not moved when deleting from a read only buffer.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
        chars: An integer representing the number of chars to delete.
    """
    og_mark = buff_read_only.mark
    buff_read_only.delete_char(chars)
    new_mark = buff_read_only.mark
    assert og_mark == new_mark


def test_delete_char_modified_read_only(buff_read_only, chars):
    """
    Check that modified state of read only buffer is False.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
        chars: An integer representing the number of chars to delete.
    """
    buff_read_only.delete_char(chars)
    assert not buff_read_only.modified


# delete_region
def test_delete_region_text(buff):
    """
    Check that region is correctly deleted from buffer.

    Args:
        buff: An Ihmacs buffer.
    """
    og_text = buff.text
    points = (buff.point, buff.mark)
    start = min(points)
    end = max(points)

    expected_text = og_text[0:start] + og_text[end:]

    buff.delete_region()

    assert expected_text == buff.text


def test_delete_region_return(buff):
    """
    Check that delete region method returns the expected text.

    Args:
        buff: An Ihmacs buffer.
    """
    og_text = buff.text
    points = (buff.point, buff.mark)
    start = min(points)
    end = max(points)

    expected_text = og_text[start:end]

    assert expected_text == buff.delete_region()


def test_delete_region_point(buff):
    """
    Check that point is moved accordingly after region delete.

    The new point should be either the og point or the og mark, whichever is
    less.

    Args:
        buff: An Ihmacs buffer.
    """
    points = (buff.point, buff.mark)
    expected_point = min(points)

    buff.delete_region()
    assert expected_point == buff.point


def test_delete_region_mark(buff):
    """
    Check that mark is moved accordingly after region delete.

    The new point should be either the og point or the og mark, whichever is
    less.

    Args:
        buff: An Ihmacs buffer.
    """
    points = (buff.point, buff.mark)
    expected_mark = min(points)

    buff.delete_region()
    assert expected_mark == buff.mark


def test_delete_region_modified(buff):
    """
    Check that modified state of buffer is True after deleting region.

    Args:
        buff: An Ihmacs buffer.
    """
    buff.delete_region()
    assert buff.modified


def test_delete_region_text_read_only(buff_read_only):
    """
    Check that nothing is deleted from a read only buffer.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
    """
    text_og = buff_read_only.text
    buff_read_only.delete_region()
    text_new = buff_read_only.text
    assert text_og == text_new


def test_delete_region_point_read_only(buff_read_only):
    """
    Check that point does not move when deleting from a read only buffer.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
    """
    og_point = buff_read_only.point
    buff_read_only.delete_region()
    new_point = buff_read_only.point
    assert og_point == new_point


def test_delete_region_mark_read_only(buff_read_only):
    """
    Check that mark is not moved when deleting from a read only buffer.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
    """
    og_mark = buff_read_only.mark
    buff_read_only.delete_region()
    new_mark = buff_read_only.mark
    assert og_mark == new_mark


def test_delete_region_modified_read_only(buff_read_only):
    """
    Check that modified state of read only buffer is False.

    Args:
        buff_read_only: An Ihmacs buffer that is read only.
    """
    buff_read_only.delete_region()
    assert not buff_read_only.modified


# append
def test_append_text(buff, insert_string):
    """
    Check string is correctly appended to buffer.

    Args:
        buff: An Ihmacs buffer.
        insert_string: A string to append to the buffer.
    """
    og_text = buff.text
    expected_text = og_text + insert_string
    buff.append(insert_string)
    assert expected_text == buff.text


def test_append_return(buff, insert_string):
    """
    Check that append returns the expected string.

    Args:
        buff: An Ihmacs buffer.
        insert_string: A string to append to the buffer.
    """
    assert insert_string == buff.append(insert_string)


def test_append_point(buff, insert_string):
    """
    Check that point is not touched after appending to buffer.

    Args:
        buff: An Ihmacs buffer.
        insert_string: A string to append to the buffer.
    """
    og_point = buff.point
    buff.append(insert_string)
    assert og_point == buff.point


def test_append_mark(buff, insert_string):
    """
    Check that mark is not touched after appending to buffer.

    Args:
        buff: An Ihmacs buffer.
        insert_string: A string to append to the buffer.
    """
    og_mark = buff.mark
    buff.append(insert_string)
    assert og_mark == buff.mark


def test_append_modified(buff, insert_string):
    """
    Check that modified state of buffer is True after appending to buffer.

    Args:
        buff: An Ihmacs buffer.
        insert_string: A string to append to the buffer.
    """
    buff.append(insert_string)
    assert buff.modified
