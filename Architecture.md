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

## Buffers

A class storing
* The text in the buffer as a string
* The point (cursor location) as an integer
* The mark (a location that is used to define a selected region) as an
  integer
* The buffer name as a string.
* A file path as a string. If the buffer is not associated with a file,
  this is the empty string.
* The major mode as a major mode object.
* *beyond MVP* The active minor modes as a list of minor mode
  objects. Minor modes would be nice but aren't needed functionality.
* A keymap for the buffer that is a combination of the major and minor
  modemaps. This maps keychords to methods.
* *beyond MVP* Kill ring (Emacs lingo for infinite clipboard)
* *beyond MVP* Buffer history (list of commands)
* *beyond MVP* A modeline as a string. Will use string formatting to
  display information about the buffer.

## Major Mode

All major modes inherent from the "fundamental" mode class. For sake of
practice, fundamental will inherit from an abstract mode.

The major mode class will contain
* Rules for syntax highlighting (would pygments work, or do I need to
  write my own for every language?)
* Rules for indentation
* A major mode map that is a map of keychords to editing commands.
* Mode specific (language specific) editing commands (methods).

## Minor Modes (Beyond MVP)

If I have time I'll implement this.

# View

Everything will be represented via ncursed in a terminal.

## Windows

A class that displays a buffer in a text pane. While Emacs allows
splitting a frame into multiple windows, I will use a single window for
simplicity.

The class will have an associated buffer (and in tern, associated major
and minor modes with that buffer for markup like syntax highlighting)

The class will need to store
- Character width of window
- Character height of window

As an MVP, I need to display the buffer text and point as a cursor.

To go beyond that, syntax highlighting and a modeline will be displayed.

# Controller

Handle terminal input via keyboard.

A way of reading keychords.

The controller class will need to know
- The active window (which has a buffer that keychords can be mapped
  to).
- Way of reading keychords, and then running the associated methods in
  the mode map.
