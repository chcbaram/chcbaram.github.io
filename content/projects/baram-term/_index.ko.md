---
title: "baram-term"
description: "펌웨어 CLI 용 시리얼 터미널. 같은 창 안에서 실시간 그래프를 그린다."
repo: "https://github.com/chcbaram/baram-term"
---

펌웨어 작업을 하면서 minicom 을 대신하려고 만든 시리얼 터미널이다. 문자 격자로 된
TUI 처럼 보이지만 실제로는 데스크톱 GUI 창이라서, 그래프를 문자가 아니라 진짜 픽셀로
그린다.

보여 주고 있는 그 포트에서 `>name:value`(Teleplot) 와 Arduino 시리얼 플로터 형식을
같이 읽고, 보드를 뽑거나 리셋하면 알아서 다시 붙고, 보드의 `help` 출력에서 명령 목록을
배워 Tab 자동완성에 쓴다.
