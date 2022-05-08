"""
Test Markov chain functions.
"""


import pytest

from markov import (
    ends_sentence,
    create_markov_chain,
    # Other functions have random behavior
)


ends_sentence_cases = [
    # Empty string
    ("", False),
    # Words that do not end sentence
    ("This", False),
    ("A", False),
    ("foo", False),
    ("this sentence is false", False),
    ("this.is", False),
    ("this?is", False),
    ("this!is", False),
    # Words that end a sentence
    ("Mr.", True),
    ("Hello!", True),
    ("Done.", True),
    ("Hello?", True),
]


create_markov_chain_cases = [
    # The empty list
    ([], {"": [""]}),
    # A basic sentence
    ("This is a test.".split(),
     {"": ["This"],
      "This": ["is"],
      "is": ["a"],
      "a": ["test."],
      "test.": [""]}),
    # A case where the last word does not have .?! as the last char
    ("this sentence is false".split(),
     {"": ["this"],
      "this": ["sentence"],
      "sentence": ["is"],
      "is": ["false"],
      "false": [""]}),
    # A case where there are multiple mappings
    ("This is a test. This sentence is false.".split(),
     {"": ["This", "This"],
      "This": ["is", "sentence"],
      "is": ["a", "false."],
      "a": ["test."],
      "test.": [""],
      "sentence": ["is"],
      "false.": [""]}),
]


@pytest.mark.parametrize("word,result", ends_sentence_cases)
def test_ends_sentence(word, result):
    """
    Test that a sentence ending word is correctly identified.

    Args:
        word: A string representing a word.
        result: A bool representing the expected outcome.
    """
    returned_result = ends_sentence(word)
    assert returned_result == result


@pytest.mark.parametrize("word_list,result", create_markov_chain_cases)
def test_create_markov_chain(word_list, result):
    """
    Test that a Markov chain is correctly created from a word list.

    Args:
        word_list: A list of strings representing training text.
        result: A dictionary representing a Markov chain representing the
            expected outcome.
    """
    returned_result = create_markov_chain(word_list)
    assert returned_result == result
