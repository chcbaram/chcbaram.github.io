---
title: "titan-mini"
description: "Renesas RA8P1 듀얼 코어 보드용 펌웨어. 1 GHz Cortex-M85, 짝을 이루는 Cortex-M33, 그리고 Ethos-U55 NPU."
repo: "https://github.com/chcbaram/titan-mini"
---

Renesas `R7KA8P1KFLCAC` 로 만든 Titan Mini 보드용 펌웨어다. CPU0 가 1 GHz 로 도는
Cortex-M85, CPU1 이 Cortex-M33, 거기에 Ethos-U55 NPU 가 붙어 있고, 289볼 BGA 에
MRAM 1 MB 와 SRAM 1872 KB 다.

목표는 보드에 달린 것을 전부 굴리는 것이다. 저장소에 회로도와 FSP 가 생성한 설정,
그리고 `firmware/docs/` 아래의 개발 기록이 같이 들어 있다.
