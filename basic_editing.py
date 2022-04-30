"""
Basic editing commands for Ihmacs.

All these functions can take custom arguments, but also a list of
keyword arguments that contains the entire state of the editor.
"""

from buff import Buffer


def self_insert_command(ihmacs_state):
    """
    Insert the character you type at point.

    Args:
        ihmacs_state: The entire global Ihmacs state as a keyarg dict.
    """
    buff = ihmacs_state["active_buff"]
    keychord = ihmacs_state["keychord"]
    # The last stroke typed in the keychord
    char = keychord[-1]
    buff.insert(char)


def insert(ihmacs_state, string):
    """
    Insert string at point in buffer.

    Args:
        buff: A buffer passed through to this command.
        keychord: A keychord passed through to this command.
        string: A string to insert into the buffer.
    """
    buff = ihmacs_state["active_buff"]
    buff.insert(string)


# TOOD: Remove this
def test_insert1(ihmacs_state):
    """
    test command, will delete later
    """
    buff = ihmacs_state["active_buff"]

    insert(ihmacs_state,
           "This would open a file, had I implemented that yet")


def kill_ihmacs(ihmacs_state):
    """
    Kills the editor.

    WARNING: DOES NOT CHECK TO SAVE

    Args:
        buff: A buffer passed through to this command.
        keychord: A keychord passed through to this command.
    """
    # TODO: Fix me

    # Now that I have the global state passthrough, this is much easier
    # to implement. Still broken for now though.
    return 1/0


def command_undefined(ihmacs_state):
    """
    Tell user typed keychord is not mapped.

    Args:
        buff: A buffer passed through to this command.
        keychord: A keychord passed through to this command.
    """
    pass


def delete_char(ihmacs_state, num=1):
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
    buff = ihmacs_state["active_buff"]

    buff.delete_char(num)


def backwards_delete_char(ihmacs_state, num=1):
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
    buff = ihmacs_state["active_buff"]

    buff.delete_char(-num)
