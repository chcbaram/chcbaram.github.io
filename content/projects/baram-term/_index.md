---
title: "baram-term"
description: "A serial terminal for firmware CLIs, with a real-time plot in the same window."
repo: "https://github.com/chcbaram/baram-term"
---

A serial terminal I wrote to replace minicom while working on firmware. It looks
like a character-grid TUI but is a desktop GUI window, so the plots are drawn in
real pixels rather than characters.

It reads `>name:value` (Teleplot) and Arduino Serial Plotter formats off the same
port it is showing, reconnects on its own when a board is unplugged or reset, and
learns the command list from the board's `help` output for Tab completion.
