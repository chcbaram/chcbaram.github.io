---
title: "baram-nrf54-arduino"
description: "Nordic nRF54L 시리즈용 Arduino 코어. 기존 Adafruit Bluefruit(nRF52) 스케치가 그대로 돌아가는 것을 목표로 만들었다."
repo: "https://github.com/chcbaram/baram-nrf54-arduino"
---

Nordic nRF54L 시리즈용 Arduino 코어다. Adafruit 의 nRF52 Bluefruit 코어용으로 쓴
스케치가 그대로 돌아가는 것이 목표라서, 자체 API 를 새로 만드는 대신 Bluefruit 를
따른다.

0.4.0 기준으로 페리페럴 API(`Wire`, `SPI`, `attachInterrupt`, `analogWrite`,
`analogRead`) 를 보드 4종에서 하드웨어로 검증했고, BLE 는 peripheral 과 central 양쪽
모두 동작한다. 부트로더는 아직 없어서 업로드에 SWD 가 필요하다.

nRF52 와 다른 점 하나. nRF54L 에서는 페리페럴이 GPIO 포트에 묶여 있어서, 핀 배정이
틀리면 런타임에 조용히 실패하는 대신 빌드가 깨진다.
