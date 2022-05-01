"""
Devlin Ihmacs editor.
"""

import curses

from ihmacs_class import Ihmacs


def main(stdscr):
    """
    Setup Ihmacs model and run.

    Args:
        stdscr: An ncurses screen object. Required for ncurses wrapper.
    """
    # Setup curses
    curses.raw()  # Raw input, doesn't translate codes like C-c to mean
    # terminate and kill the program

    # Clear screen at start
    stdscr.clear()

    # Create instance of editor and run
    ihmacs = Ihmacs(stdscr)
    ihmacs.run()


# Run the program
curses.wrapper(main)
