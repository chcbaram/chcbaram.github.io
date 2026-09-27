---
title: "wish-he"
description: "시판 홀 이펙트 키보드용 커스텀 펌웨어. QMK 와 VIA 를 손대지 않고 그대로 쓰면서 밑에서 키 판정만 바꿔 끼운다."
repo: "https://github.com/chcbaram/wish-he"
---

시판 홀 이펙트 키보드용 커스텀 펌웨어다. HPM5361(RISC-V, 400 MHz) 에서 돈다. QMK 와
VIA 를 가능한 한 손대지 않고 포팅하고 홀 이펙트 부분을 그 밑에 끼워 넣어서, 레이어와
매크로와 탭홀드와 키 오버라이드와 조명이 키별 아날로그 설정과 함께 그대로 동작한다.

바꿔 끼우는 것은 키 판정뿐이다. 결과를 매트릭스 계층에서 QMK 에 넘기므로 그 위쪽은
바꿀 것이 없고, VIA 는 프로토콜을 흉내 낸 물건이 아니라 QMK 자신의 `via.c` 를 통해
붙는다. 디바운스는 없다. 튈 접점이 없다.

전용 PCB 는 없다. Geonworks VENOM60HE 7U(`wish60-he-7u`, 63키, 83 LED) 와
EverGlide AE61 Pro(`wish61-he`, 61키, 104 LED) 에서 돌고, 각 보드의 원래 IAP
부트로더를 그대로 남겨 두어서 언제든 순정으로 되돌릴 수 있다. 설정과 굽기는
브라우저에서 [via-he](https://chcbaram.github.io/via-he/) 로 한다.
