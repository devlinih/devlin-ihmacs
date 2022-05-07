"""
Test tree helper functions.
"""

# Does not actually have any tests right now, I just wanted to save the
# test tree I made for experimenting

test_tree_1 = (
    {i: "self_insert_command"
     for i in ascii_letters+digits+punctuation+" "} |
    {"C-j": "newline",
     "DEL": "backwards_delete_char",  # Backspace
     "KEY_DC": "delete_char",  # Delete
     "C-d": "delete_char",
     "C-f": "forward_char",
     "KEY_RIGHT": "forward_char",
     "M-f": "forward_word",
     "C-b": "backward_char",
     "KEY_LEFT": "backward_char",
     "M-b": "backward_word",
     "C-n": "next_line",
     "KEY_DOWN": "next_line",
     "C-p": "previous_line",
     "KEY_UP": "previous_line",
     "C-a": "move_beginning_of_line",
     "KEY_HOME": "move_beginning_of_line",
     "C-e": "move_end_of_line",
     "KEY_END": "move_end_of_line",
     "C-v": "scroll_up",
     "KEY_NPAGE": "scroll_up",
     "M-v": "scroll_down",
     "KEY_PPAGE": "scroll_down",
     "C-x": {"C-f": "find_file",
             "C-c": "kill_ihmacs",
             "p": {"f": "project_find_file",
                   "p": "project_switch_project", }, },
     "C-c": {"C-c": "send-buffer",
             "m": "mu4e", }, }
)
