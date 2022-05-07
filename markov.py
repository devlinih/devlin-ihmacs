"""
Markov chain text generation for Devlin Ihmacs.
"""

import random


def ends_sentence(word):
    """
    Test if word ends sentence.

    The end of a sentence is defined by a word ending with a period,
    exclamation point, or a question mark.

    Args:
        word: A string representing a word.

    Returns:
        A bool representing if the word ends a sentence.
    """
    return word[-1] in ".?!"


def create_markov_chain(word_list):
    """
    Generate a Markov chain from a set of messages.

    Create a dictionary mapping a word (represented by a string), to a list of
    words that follow it (list of strings). "" represents the start of a
    sentence.

    This function assumes the last word of the list ends a sentence, even if it
    does not.

    If passed the empty list, return a dictionary mapping the empty string to
    a list with the empty string.

    Args:
        word_list: A list of strings representing all words in all of the
            training messages.

    Returns:
        A dictionary representing a Markov chain.
    """
    # Check if the word list is empty
    if word_list == []:
        return {"": [""]}

    # Initialize the dictionary
    markov = {}

    # The first word of the input is assumed to start a sentence.
    markov[""] = [word_list[0]]

    # Iterate through the word list.
    word_list_length = len(word_list)
    for i in range(word_list_length - 1):
        current_word = word_list[i]
        next_word = word_list[i + 1]

        # Initialize entry as a list if it does not exist yet.
        if current_word not in markov:
            markov[current_word] = []

        # Check if the current word ends a sentence.
        if ends_sentence(current_word):
            markov[current_word] = [""]
            markov[""].append(next_word)
        else:
            markov[current_word].append(next_word)

    # Deal with the last word
    last_word = word_list[-1]
    if last_word not in markov:
        markov[last_word] = []
    markov[last_word].append("")

    return markov


def generate_sentence(markov):
    """
    Generate a random sentence from a Markov chain.

    Assumes some words in the Markov chain map to "". If not, this will loop
    infinitely.

    Args:
        markov: A dictionary mapping strings to lists of strings representing
            a Markov chain.

    Returns:
        A string containing a randomly generated sentence.
    """
    # Init list
    sentence_words = []
    current_word = ""

    while True:
        current_word = random.choice(markov[current_word])
        if current_word == "":
            break
        sentence_words.append(current_word)

    return " ".join(sentence_words)


def generate_sentence_from_text(text, num=1):
    """
    Generate N random sentences based on a text.

    Uses a Markov chain to generate these sentences.

    Args:
        text: A string representing the training text.
        num: An integer representing the number of sentences to generate. If
            0 or negative, generate no sentences.

    Returns:
        A string representing the generated sentences.
    """
    word_list = text.split()
    markov = create_markov_chain(word_list)

    # Generate text
    text_to_insert = ""
    while num > 0:
        text_to_insert = text_to_insert + generate_sentence(markov)
        num -= 1
    return text_to_insert
