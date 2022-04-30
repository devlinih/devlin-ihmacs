"""
Basic editing commands for Ihmacs.

All these functions can take custom arguments, but the first argument
must be an Ihmacs object containing the global state of the editor.
"""

from buff import Buffer


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
