---
title: "wish-he"
description: "Custom firmware for commercial Hall-effect keyboards, running QMK and VIA unchanged with the key decision swapped out underneath."
repo: "https://github.com/chcbaram/wish-he"
---

Custom firmware for commercial Hall-effect keyboards, running on an HPM5361
(RISC-V, 400 MHz). QMK and VIA are ported with as little change as possible and
the Hall-effect part is fitted underneath, so layers, macros, tap-hold, key
overrides and lighting all keep working alongside per-key analog settings.

Only the key decision is replaced. QMK is handed the result at the matrix layer,
so nothing above it needs to change, and VIA connects through QMK's own `via.c`
rather than an imitation of the protocol. There is no debounce — there are no
contacts to bounce.

No PCB of its own. It runs on the Geonworks VENOM60HE 7U (`wish60-he-7u`, 63 keys,
83 LEDs) and the EverGlide AE61 Pro (`wish61-he`, 61 keys, 104 LEDs), and leaves
each board's original IAP bootloader in place, so a board can be returned to stock.
Configuration and flashing happen in the browser through
[via-he](https://chcbaram.github.io/via-he/).
