# Devlin Ihmacs

Devlin Ihmacs is an Emacs-like text editor implemented in Python 3. It
is written by Devlin Ih.

Check out the source code for the project
[here.](https://github.com/olincollege/devlin-ihmacs)


# Features

- A curses based interface

- Multiple text buffers

- Familiar Emacs keybindings (if you're familiar with Emacs keybindings)

- Select regions via point and mark (although the region is not
  highlighted)

- Markov chain based text generation (I couldn't resist)

- Around 900 source lines of code of Python 3


# Obligatory Animated GIF Section

TODO


# Installation

## Dependencies

Devlin Ihmacs has no dependencies other than Python 3 and ncurses. All
functionality is implemented through the Python standard library
(curses, regex). Most Linux and Unix distributions should have this
installed. If you are on Windows with WSL, Devlin Ihmacs *should*
run. If you are on native Windows, sorry.

## Installation

1. Download an archive of the source or clone this repository. `git
   clone https://github.com/olincollege/devlin-ihmacs.git`

2. Change directory to the project root.

3. Run `python ihmacs.py`. You will be placed into a scratch buffer. You
   can exit by typing `C-x` `C-c`.


# Usage

## Keybindings

For those not familiar with Emacs style keybindings and notation, here's
a brief rundown.

A single keystroke looks something like this: `C-x`. The `C-`
means the CONTROL key is being held down. `M-` means the META key is
held down (a historical term, ALT is bound to META). So `C-M-x` means
CONTROL, ALT, and x were pressed at the same time.

Editing commands have bindings to "keychords." A keychord is a
sequence of keystrokes. For example, the keychord `C-x` `C-c` binds do
the command `kill_ihmacs`.

A brief note: the program you call a "terminal" is actually a "terminal
*emulator*," this is because it is emulating a piece of hardware made
over 50 years ago. Because of this and the way the ncurses library
handles input, there are some limitations on the keystrokes that are
allowed. For example, `RET`, `C-j`, and `C-m` all send the same
signal. `C-i` and `TAB` also send the same signal. Pressing `ESC` is a
sort of "sticky-keys" version of meta. This is because `M-` combinations
are indicated by sending an escape character.

And with that out of the way, here are the keybindings implemented in
Devlin Ihmacs.

| Keychord            | Command                         | Description                                   |
|---------------------|---------------------------------|-----------------------------------------------|
| Alphanumeric keys   | `self_insert_command`           | Insert the typed character                    |
| `C-j`/`RET`/`C-m`   | `newline`                       | Insert a newline                              |
| `DEL` (backspace)   | `backwards_delete_char`         | Delete character before point                 |
| `KEY_DC` (delete)   | `delete_char`                   | Delete character after point                  |
| `C-d`               | `delete_char`                   | ^                                             |
| `C-f`               | `forward_char`                  | More point (cursor) forward 1 char            |
| `KEY_RIGHT`         | `forward_char`                  | ^                                             |
| `M-f`               | `forward_word`                  | Move point forward 1 word                     |
| `C-b`               | `backward_char`                 | Move point backward 1 char                    |
| `M-b`               | `backward_word`                 | Move point backward 1 word                    |
| `C-n`               | `next_line`                     | Move point down 1 line                        |
| `KEY_DOWN`          | `next_line`                     | ^                                             |
| `C-p`               | `previous_line`                 | Move point up one line                        |
| `KEY_UP`            | `previous_line`                 | ^                                             |
| `C-a`               | `move_beginning_of_line`        | Move point to start of line                   |
| `KEY_HOME`          | `move_beginning_of_line`        | ^                                             |
| `C-e`               | `move_end_of_line`              | Move point to end of line                     |
| `KEY_END`           | `move_end_of_line`              | ^                                             |
| `C-v`               | `scroll_up`                     | Scroll text on screen up                      |
| `KEY_NPAGE`         | `scroll_up`                     | ^                                             |
| `M-v`               | `scroll_down`                   | Scroll text on screen down                    |
| `KEY_PPAGE`         | `scroll_down`                   | ^                                             |
| `C-k`               | `kill_line`                     | Kill (cut) text from point to end of line     |
| `C-y`               | `yank`                          | Yank (paste) latest entry in kill ring        |
| `C-SPC`             | `set_mark_command`              | Set mark to location of point                 |
| `C-x` `C-x`         | `exchange_point_and_mark`       | Swap locations of point and mark              |
| `C-w`               | `kill_region`                   | Kill text between point and mark              |
| `M-w`               | `kill_ring_save`                | Copy text between point and mark              |
| `M-DEL` (backspace) | `backward_kill_word`            | Kill from point to start of word              |
| `M-d`               | `forward_kill_word`             | Kill from point to end of word                |
| `M-<`               | `beginning_of_buffer`           | Move point to start of buffer                 |
| `M->`               | `end_of_buffer`                 | Move point to end of buffer                   |
| `C-c` `C-j`         | `generate_sentence_from_buffer` | Generate random sentence based on buffer text |
| `C-x` `C-f`         | `create_buffer`                 | Create a new virtual buffer                   |
| `C-x` `b`           | `next_buffer`                   | Switch to next virtual buffer                 |
| `C-x` `C-b`         | `previous_buffer`               | Switch to previous virtual buffer             |
| `C-x` `k`           | `kill_buffer`                   | Close active buffer                           |
| `C-x` `C-c`         | `kill_ihmacs`                   | Close the editor                              |



# About Me

I am Devlin Ih. "Ih" is pronounced like the letter "E." Thus, "Ihmacs"
is pronounced exactly like "Emacs."

I'm a student (CO 2025) at Olin College of Engineering in Needham
Massachusetts.

Good talk.
