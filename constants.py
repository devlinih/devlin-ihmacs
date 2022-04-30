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
    {"C-x": {"C-f": test_insert1,  # Replace this with find file
             "C-c": kill_ihmacs,
             }
     }
)
