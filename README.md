# Devlin Ihmacs

Devlin Ihmacs is an Emacs-like text editor implemented in Python 3. It
aims to reproduce the look and feel of Emacs by implementing an editing
model based on buffers and modes.

[Project Site](https://olincollege.github.io/devlin-ihmacs)


# Pronunciation

The name of this project is a pun on Emacs and my last name. "Ih" is
pronounced like the letter E. Ihmacs is pronounced like Emacs. In order
to distinguish this from other Emacsen, I threw my first name
in front of it.


# Features

- A curses based interface

- Multiple text buffers

- Familiar Emacs keybindings (if you're familiar with Emacs keybindings)

- Select regions via point and mark (although the region is not
  highlighted)

- Markov chain based text generation (I couldn't resist)

- Around 900 source lines of code of Python 3


## Unfortunately Missing Features

- File IO. While the buffer class has methods for reading and writing
  files, they are in an incomplete state that is not ready for
  keybindings yet. All buffers are virtual.

- Minibuffer input. As a consequence, many features such as `M-x`
  (`execute-extended-command`) are missing. In addition, commands for
  switching buffer cycle through buffers rather than interactively
  asking the user for a buffer to switch to.

- Minor modes

- Major modes other than fundamental mode (no syntax highlighting or
  language specific features)

- Universal argument (if you know GNU Emacs, this will make you
  sad). That means for example that while under the hood Devlin Ihmacs
  is storing an infinite kill ring with every copy and kill operation
  you have done, it can only pull the latest kill. So effectively, there
  is no infinite clipboard even though it's storing one 🙃


# Notes about the code

## Files

The source code is split into the following files (in alphabetical
order):


### basic_editing.py

Contains all editing commands that manipulate global and buffer
state. Also contains the definition for the default global keymap.


### buff.py

Contains the `Buffer` class definition, which stores the state of a text
buffer.


### controller.py

Contains the `Controller` class definition, which has facilities to read
keyboard input and execute editing commands.


### fundamental_mode.py

Contains the definition of `FundamentalMode` class, the only major mode
implemented thus far in Devlin Ihmacs.


### ihmacs.py

Ties everything together in a way that can be executed. The purpose of
this file is to bootstrap the editor. Running `python ihmacs.py` at the
command line starts Devlin Ihmacs.


### ihmacs_class.py

Contains the definition for the `Ihmacs` class, which is used to hold
the global state of the editor.


### markov.py

Contains function definitions for generating non-sense sentences via a
Markov chain. I couldn't help myself.


### tree_helpers.py

Contains function definitions for working with dictionary trees. This
file exists to make it easier to work with keymaps. In addition, there
is a predicate function to compare function docstrings. This is a
workaround for having multiple instances of the same function in
memory.


### view.py

Contains the `View` class definition, which has facilities for
displaying text buffers, the modeline, and echoing messages to the
screen.


## Hardcoding

Unfortunately, there are a few hardcoded values in the code. First is
the newline character `"\n"`. This string is frequently used in various
functions. Not only is this a magic number, it also assumes a Unix file
encoding.

The ncurses view also has some hardcoded values. For example, it assumes
the modeline is to be displayed on the second to last line, so there are
a lot of arbitrary looking `- 2`s in the code. The view could use a
complete rewrite using multiple ncurses windows and splitting. This
would be cleaner, less dependent on this hardcoding, and could lead to
multiple buffers being displayed side by side (`C-x` `2` and `C-x` `3`
in GNU Emacs).


## Unit Tests

Unit tests are included for `basic_editing.py`, `buff.py`,
`fundamental_mode.py`, `markov.py`, and `tree_helpers.py`. The functions
which mutate classes use fixtures to generate a very comprehensive list
of tests (over 32000) that actually caught some mistakes of mine!. The
tests for `markov.py` and `tree_helpers.py` were hand created, as those
functions do not mutate state at all and are easy to test without
obscene amounts of cases.

Certain functions, classes, and methods were not tested for various
reasons. curses applications are hard to unit test input and
output. Functions with random behavior were not tested. Lastly, regex
functions were not tested as they mutate the state and would thus need
many comprehensive tests. Unfortunately, the only way to test that with
the fixtures would be re-implementing the regex move
commands. Unfortunately, testing a function against an identical
implementation of the same thing would teach you nothing.


# Installation and Usage

## Dependencies

Devlin Ihmacs has no dependencies other than Python 3 (3.9 or later) and
ncurses. All functionality is implemented through the Python
[curses](https://docs.python.org/3/library/curses.html) bindings and
[regular expressions](https://docs.python.org/3/library/re.html), both
of which are included in the Python standard library. Most Linux and
Unix distributions should have everything installed. If you are on
Windows with WSL, Devlin Ihmacs *should* run.

If you are on native Windows, sorry, Python does not include the
curses module. It might be possible to run with slight modifications
using [UniCurses](https://pypi.org/project/UniCurses/), although this
has not been tested.


## Installation

1. Download an archive of the source or clone this repository. `git
   clone https://github.com/olincollege/devlin-ihmacs.git`

2. Change directory to the project root.

3. Run `python ihmacs.py`. You will be placed into a scratch buffer. You
   can exit by typing `C-x` `C-c`.


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
