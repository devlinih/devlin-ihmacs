# Editing Commands in GNU/Emacs in Fundamental Mode

These were pulled right from GNU/Emacs

# Every C-alphanumeric key

Avoiding punctuation here because those have funky results.

`C-backtic (thanks markdown)` undefined
`C-0123456789` digit-argument
`C-q` quoted-insert (crap, I don't want to rewrite the controller again)
`C-w` kill-region
`C-e` move-end-of-line
`C-r` isearch-backward
`C-t` transpose-chars
`C-y` yank
`C-u` universal-argument
`C-i` indent-for-tab-command
`C-o` open-line
`C-p` previous-line
`C-a` move-beginning-of-line
`C-s` isearch-forward
`C-d` delete-char
`C-f` forward-char
`C-g` keyboard-quit
`C-h` help prefix command
`C-j` electric-newline-maybe-indent
`C-k` kill-line
`C-l` recenter-top-bottom
`C-z` suspend (no)
`C-x` extended command prefix
`C-c` user/mode prefix
`C-v` scroll-up-command
`C-b` backward-char
`C-n` next-line
`C-m` newline
`C-SPC` set-mark-command

# Every M-alphanumeric/punct (with some exceptions)

Every key EXCEPT `[` (and to avoid confusion `]` and `\`) on the 60% layout part of the board. Gets funky with the nav cluster.

`M-backtic` tmm-menubar
`M-0123456789` digit-argument
`M--` negative-argument
`M-=` count-words-region
`M-DEL` backward-kill-word
`M-TAB` (`C-M-i`) complete-symbol
`M-q` fill-paragraph
`M-w` kill-ring-save
`M-e` forward-sentence
`M-r` move-to-window-line-top-bottom
`M-t` transpose-words
`M-y` yank-pop
`M-u` upcase-word
`M-i` tab-to-tab-stop
`M-o` unbound
`M-p` unbound
`M-a` backward-sentence
`M-s` isearch prefix
`M-d` kill-word
`M-f` forward-word
`M-g` movement (go) prefix
`M-h` mark-paragraph
`M-j` default-indent-new-line
`M-k` kill-sentence
`M-l` downcase-word
`M-;` comment-dwim (do what I mean)
`M-'` abbrev-prefix-mark (I am not dong abbrev mode that's not happening)
`M-z` zap-to-char
`M-x` execute-extended-command (gonna be hard with my architecture)
`M-c` capitalize-word
`M-v` scroll-down-command
`M-b` backward-word
`M-n` unbound
`M-m` back-to-indentation
`M-,` xref-pop-marker-stack
`M-.` xref-find-definitions (yeah no not implementing xref)
`M-/` dabbrev-expand (not doing dabbrevs)
`M-SPC` just-one-space
