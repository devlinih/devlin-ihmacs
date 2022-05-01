"""
ncurses testing file.

Used to find what codes will be returned for different keystrokes.
"""

import curses


def main(window):
    """
    Main loop for testing script
    """
    curses.raw()
    # window.keypad(False)

    key = [-1]

    while key[0] != ord("q"):
        key = get_key(window)
        window.clear()
        window.addstr(0, 0, str(key))

        if key[0] == 27:
            # meta = "M-"
            facekey = key[1]
        else:
            # meta = ""
            facekey = key[0]

        facekey = curses.keyname(facekey)
        window.addstr(1, 0, facekey.decode("utf-8"))

        window.refresh()


def get_key(window):
    """
    Read a keystroke from the terminal.
    """
    key = []
    char = window.getch()
    key.append(char)

    window.nodelay(True)
    while char != -1:
        char = window.getch()
        key.append(char)

    window.nodelay(False)

    return key


curses.wrapper(main)
