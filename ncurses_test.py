"""
ncurses testing file.

Used to find what codes will be returned for different keystrokes.
"""

import curses


def main(window):
    curses.raw()
    # window.keypad(False)

    key = [-1]

    while key[0] != ord("q"):
        key = get_key(window)
        window.clear()
        window.addstr(0, 0, str(key))

        if key[0] == 27:
            meta = "M-"
            facekey = key[1]
        else:
            meta = ""
            facekey = key[0]

        facekey = curses.keyname(facekey)
        window.addstr(1, 0, facekey.decode("utf-8"))

        window.refresh()


def get_key(window):
    key = []
    char = window.getch()
    key.append(char)

    while char != -1:
        window.nodelay(True)
        try:
            char = window.getch()
            key.append(char)
        except:
            char = False

    window.nodelay(False)

    return key


curses.wrapper(main)
