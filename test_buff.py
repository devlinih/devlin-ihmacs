"""
Unit tests for Buffer class.
"""

import pytest

from buff import Buffer


@pytest.fixture
def buff():
    """
    Create an Ihmacs text buffer for use in testing.
    """
    return Buffer()


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


def test_insert_text(buff, insert_string):
    """
    Check that text is correctly inserted into the buffer.

    Args:
        buff: An Ihmacs buffer.
    """
    buff.insert(insert_string)
    assert buff.text == insert_string
