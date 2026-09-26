---
title: "titan-mini"
description: "Firmware for a Renesas RA8P1 dual-core board: Cortex-M85 at 1 GHz, a Cortex-M33 companion, and an Ethos-U55 NPU."
repo: "https://github.com/chcbaram/titan-mini"
---

Firmware for the Titan Mini board, built around the Renesas `R7KA8P1KFLCAC` —
a Cortex-M85 running at 1 GHz as CPU0, a Cortex-M33 as CPU1, and an Ethos-U55
NPU, in a 289-ball BGA with 1 MB of MRAM and 1872 KB of SRAM.

The goal is to drive everything on the board. The repository carries the
schematics, the FSP-generated configuration, and a development log under
`firmware/docs/`.
