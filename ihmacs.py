"""
Devlin Ihmacs editor.
"""

from ihmacs_class import Ihmacs

import curses

def main(stdscr):
    """
    Setup Ihmacs model and run.

    Args:
        stdscr: An ncurses screen object. Required for ncurses wrapper.
    """
    # Setup curses
    curses.raw() # Raw input, doesn't translate codes like C-c to mean
                 # terminate and kill the program
    stdscr.keypad(False) # Chose to read inputs directly, was having
                         # issues with alt/meta

    # Clear screen at start
    stdscr.clear

    # Create instance of editor and run
    ihmacs = Ihmacs(stdscr)
    ihmacs.run()


# Run the program
curses.wrapper(main)
