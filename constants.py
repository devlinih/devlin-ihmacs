"""
Constants used at various places in the Ihmacs editor.

Defined here to avoid clutter in other files.
"""

from basic_editing import *

import curses


from string import (
    ascii_letters,
    digits,
    punctuation,
)

DEFAULT_GLOBAL_KEYMAP = (
    {i: self_insert_command
     for i in ascii_letters+digits+punctuation+" "} |
    {"C-j": newline,
     "DEL": backwards_delete_char,
     "C-f": forward_char,
     "KEY_RIGHT": forward_char,
     "C-b": backward_char,
     "KEY_LEFT": backward_char,
     # Extended commands
     "C-x": {"C-f": find_file,
             "C-c": kill_ihmacs, }, }
)
