"""
Major mode class for Ihmacs.

All major modes inherit from FundamentalMode class.
"""

# Regex will be used to try to guess indentation, etc
import re


class FundamentalMode:
    """
    The most basic editing mode.

    Contains no syntax highlighting rules, indentation rules, or keymap.

    Attributes:
        keymap: A dictionary of dictionaries representing the modemap.
    """

    keymap = {}

    def __init__(self):
        """
        Initialize fundamental mode.
        """
        pass

    def indent_line(self, pos, buff):
        """
        Indents a line in a buffer.

        Args:
            pos: An integer representing a location in a buffer.
            buff: An Ihmacs buffer object.
        """
        pass
