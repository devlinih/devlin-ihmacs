"""
Devlin Ihmacs editor.
"""

from ihmacs_class import Ihmacs

from curses import wrapper


def main(stdscr):
    """
    Setup Ihmacs model and run.

    Args:
        stdscr: An ncurses screen object. Required for ncurses wrapper.
    """
    # clear screen
    stdscr.clear

    ihmacs = Ihmacs(stdscr)
    ihmacs.run()


wrapper(main)
