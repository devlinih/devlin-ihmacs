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
        _name: A string representing a printed name of the mode.
        _modemap: A dictionary of dictionaries representing the modemap. This
            is the keymap specific to the mode.
        _word_delimiters: A list of regular expressions used to represent what
            the word delimiters are for the given mode. This is a list because
            it's easier to expand or delete for other modes.
        _word_delimiters_regex: A regex that is compiled from combining
            everything in word_delimiters. Everything in word delimiters is
            wrapped between "[" and "]+".
    """

    _name = "Fundamental"
    _modemap = {}
    # Words are separated by whitespace, dashes, and underscores
    _word_delimiters = [r"\s", r"\-", r"_"]

    def __init__(self):
        """
        Initialize fundamental mode.
        """
        # Compile the regex.
        delimiters = self._word_delimiters
        regex_string = "[" + "".join(delimiters) + "]+"
        self._word_delimiters_regex = re.compile(regex_string)

    # Properties
    @property
    def name(self):
        """
        Return the name of the mode as a string.
        """
        return self._name

    @property
    def modemap(self):
        """
        Return the modemap dictionary.
        """
        return self._modemap

    @property
    def word_delimiters(self):
        """
        Return the word delimiters list.
        """
        return self._word_delimiters

    @property
    def word_delimiters_regex(self):
        """
        Return the word delimiters regex.
        """
        return self._word_delimiters_regex
