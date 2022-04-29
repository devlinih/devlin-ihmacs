"""
Basic editing commands for Ihmacs.

All functions here must take the same first arguments of a buffer type,
and a keychord.
"""

from buff import Buffer


def self_insert_command(buff, keychord):
    """
    Insert the character you type at point.

    Args:
        buff: A buffer passed through to this command.
        keychord: A keychord passed through to this command.
    """
    # The last character typed in the keychord
    char = keychord[-1]
    buff.insert(char)

def insert(buff, keychord, string):
    """
    Insert string at point in buffer.

    Args:
        buff: A buffer passed through to this command.
        keychord: A keychord passed through to this command.
        string: A string to insert into the buffer.
    """
    buff.insert(string)


# TOOD: Remove this
def test_insert1(buff, keychord):
    """
    test command, will delete later
    """
    insert(buff, keychord,
           "This would open a file, had I implemented that yet")


def kill_ihmacs(buff, keychord):
    """
    Kills the editor.

    WARNING: DOES NOT CHECK TO SAVE

    Args:
        buff: A buffer passed through to this command.
        keychord: A keychord passed through to this command.
    """
    # Okay, so my import crashed the program when I used break so uh,
    # let's just do something illegal instead lol
    return 1/0


def command_undefined(buff, keychord):
    """
    Tell user typed keychord is not mapped.

    Args:
        buff: A buffer passed through to this command.
        keychord: A keychord passed through to this command.
    """
    pass


def delete_char(buff, keychord, num=1):
    """
    Delete num characters at point.

    If num is positive, delete characters after point. If num is negative,
    delete characters before point.

    Args:
        buff: A buffer passed through to this command.
        keychord: A keychord passed through to this command.
        num: An integer representing how many characters to delete. The sign
            denotes the direction.
    """
    buff.delete_char(num)


def backwards_delete_char(buff, keychord, num=1):
    """
    Delete num characters at point.

    If num is negative, delete characters after point. If num is positive,
    delete characters before point.

    Args:
        buff: A buffer passed through to this command.
        keychord: A keychord passed through to this command.
        num: An integer representing how many characters to delete. The sign
            denotes the direction.
    """
    buff.delete_char(-num)
