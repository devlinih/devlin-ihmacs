# Project Architecture

# Overview

Devlin Ihmacs is an Emacs-like text editor implemented in Python. As a
MVP, it needs to be able to load text from a file in a buffer,
manipulate the buffer via the keyboard, and write the edited buffer to a
file.

# Interactivity

Ihmacs is controlled via the keyboard in a terminal environment. Editing
functions (or methods) will be mapped to via the mode map.

# Model

Editing functions are defined globally as well, functions and take in a
buffer class as an argument. They can then run buffer methods on the
passed buffer to manipulate it, as well as other functions defined
globally.

## Ihmacs

A class representing the global state of the editor.

Note: I am not implementing the concepts of multiple frames, nor even
split windows. That would be beyond the scope of this project. There
will just be one "active" buffer which is focused.

Things implemented here
* Kill ring, a list of strings representing text that has been killed
  (infinite clipboard baby!)
* Buffers, a list of all active buffers.
* Global keymap

## Buffers

A class storing
* text: A string representing the text in the buffer
* modified: A bool representing if the buffer has been modified since
  last save.
* point: An int representing cursor position
* mark: An int representing the position of the mark (define region for
  selection for those not familiar with Emacs)
* name: A string representing buffer name.
* path: A string representing the buffer file path. If the buffer is not
  associated with a file, this is the empty string.
* major_mode: The major mode as a major mode object.
* *beyond MVP* minor_modes: The active minor modes as a list of minor
  mode objects. Minor modes would be nice but aren't needed
  functionality.
* keymap: Buffer keymap, derived from combining the global keymap and
  the modemaps.
* *beyond MVP* history: A list of commands that have been executed on the
  buffer. Uses a list as a stack.
* *beyond MVP* modeline: A string that is displayed in the modeline
  (format method applied). Shows information like current line, active
  major and minor modes, etc.
* display_line: An int representing where the view of the buffer starts
  in a window. This line is the first line in the window.

## Major Mode

All major modes inherent from the "fundamental" mode class.

The major mode class will contain
* Rules for syntax highlighting (would pygments work, or do I need to
  write my own for every language?)
* Rules for indentation
* A major mode map that is a map of keychords to editing commands.
* Mode specific (language specific) editing commands (methods).

## Minor Modes (Beyond MVP)

If I have time I'll implement this.

# View

Everything will be represented via ncurses in a terminal.

There will be one frame (although this is not part of the model) and
that frame will have one window (again, not part of the model). Multiple
frames and splitting frames into windows is beyond the scope of this.

There will be a modeline at the bottom of the screen, a single line of
text, 2nd to last line.

There will be the "echo area"/"minibuffer" on the last line. This is
where new messages are displayed and where you can input text for
commands that take input (say something like `M-x`
(`execute_extended_command`)).

The frame will contain the text of the active buffer in the window.

# Controller

Handle terminal input via keyboard.

Read keychords and map them to the map.
