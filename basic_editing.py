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
        keychord: The keychord passed through to this command.
    """
    # The last character typed in the keychord
    char = keychord[-1]
    buff.insert(char)


def command_undefined(buff, keychord):
    """
    Tell user typed keychord is not mapped.
    """
    pass
