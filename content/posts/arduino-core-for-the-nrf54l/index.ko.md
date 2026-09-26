---
title: "Bluefruit 호환을 우선한 nRF54L Arduino 코어"
date: 2026-09-27T03:00:22+09:00
description: "이미 있는 코어를 쓰지 않고 nRF54L 용 Arduino 코어를 직접 만든 이유, 베어메탈 SDK 와 인증받은 SoftDevice 위에 어떻게 쌓았는지, 그 선택으로 무엇을 얻고 무엇을 잃는지."
projects: ["baram-nrf54-arduino"]
tags: ["nrf54l", "arduino", "ble", "freertos", "softdevice", "firmware"]
series: ["nRF54L Arduino Core"]
repo: "https://github.com/chcbaram/baram-nrf54-arduino"
image: "01-software-stack.png"
ai_assisted: true
naver_url: "https://blog.naver.com/chcbaram/224404179335"
draft: false
---

nRF54L 은 nRF52 의 후속이다. 그리고 nRF52 에는 Arduino BLE 코드 자산이 가장 많이
쌓여 있다 — Adafruit 의 Bluefruit 생태계다. 그런데 그게 그냥은 넘어오지 않는다.
그래서 "그냥 넘어와야 한다"를 첫 번째 규칙으로 삼은 Arduino 코어를 만들었다.

## 무엇이 문제였나

지금까지 나온 nRF54L Arduino 시도들은 전부 제3의 자체 BLE API 를 노출한다. 그것도
합리적인 선택이지만, 결과적으로 잘 돌던 nRF52 스케치를 처음부터 다시 써야 하고
`Bluefruit.begin()` 위에 쌓아 둔 라이브러리와 예제가 새 칩에서는 아무 가치가 없다.

그래서 반대쪽에 서기로 하고, 프로젝트가 깰 수 없는 규칙으로 적어 두었다.

> 이식성과 Adafruit 호환이 충돌하면 호환을 택한다.

Bluefruit Feather 용으로 짠 `.ino` 가 nRF54L 보드에서 최소 수정으로 컴파일되고
동작하는 것이 목표다 — 같은 `Bluefruit` API, 같은 `Scheduler.startLoop()`,
FreeRTOS 위에서 같은 의미로 도는 `delay()`.

설계를 그만큼 좌우한 두 번째 목표는 커스텀 보드다. 직접 만든 보드에 펌웨어를 넣고
필드에서 UART 나 BLE 로 업데이트하는 데에, 모든 유닛마다 디버그 프로브가 붙어 있어야
할 이유는 없다.

## 어떻게 쌓았나

![BARAM nRF54L Arduino 코어의 소프트웨어 스택. 스케치부터 칩까지](01-software-stack.png)

이 구조에서 의도적으로 정한 것이 셋 있다.

**베이스가 Zephyr 가 아니라 베어메탈이다.** nRF54L 시리즈용 베어메탈 옵션인
[nrfconnect/sdk-nrf-bm](https://github.com/nrfconnect/sdk-nrf-bm) v2.0.1 위에
올렸다. 스케치가 주소 0 에서 시작하는 독립 바이너리로 남고, 그래서 나중에 UART DFU
부트로더를 붙이기가 자연스럽다. 설치도 가볍고, 큰 SDK 의 릴리스 주기에 빌드가
묶이지도 않는다.

**FreeRTOS 는 선택이 아니다.** Bluefruit 의 `delay()` 와 `Scheduler.startLoop()` 가
그 의미대로 도는 건 아래에 스케줄러가 있기 때문이다. 빼면 이 프로젝트가 존재하는
이유인 호환성이 무너지므로, 취향이 아니라 규칙으로 못박았다.

**추상화 레이어를 하나 더 두지 않는다.** Bluefruit API 와 Arduino API 자체가 이미
경계면이다. 그 아래에 HAL 을 하나 더 만드는 건 추상화를 위한 추상화라서 만들지 않았다.

BLE 스택은 Nordic 의 SoftDevice S145 v10.0.1 이다. peripheral 과 central 을 모두
지원하고 Bluetooth 인증을 받은 물건이며, 자체 구현이 아니다.

## 그래서 무엇을 얻나

- **설치가 가볍다.** 플랫폼 아카이브가 1.7 MB 고, Board Manager 가 Arm 툴체인과
  `probe-rs` 까지 같이 깐다. Python 도, SDK 도, `west` 도 필요 없다. SDK 기반
  툴체인은 첫 설치가 수 GB 다.
- **슬립 중에도 시간이 어긋나지 않는다.** FreeRTOS 가 GRTC 틱으로 tickless 하게
  돌고, 하드웨어 SYSCOUNTER 대비 0.0 ppm 으로 실측됐다.
- **결과물도 작다.** blink + `Serial` + 태스크 2개가 플래시 38,004 B, RAM 3,856 B 다.
- **BLE 가 맛보기 수준이 아니다.** 광고, 커스텀 서비스를 포함한 GATT 서버,
  `BLEUart` · `BLEDis` · `BLEBas`, ATT MTU 247, central 로서의 스캔과 연결,
  LE Secure Connections 를 포함한 페어링·본딩, HID, BLE-MIDI, ANCS 까지 된다.
  동시 연결은 nRF54L15 에서 5개, nRF54L05 에서 3개분 RAM 을 잡아 둔다.
- **보드 4종, 그중 둘은 USB-C 하나면 끝.** XIAO 두 장과 NU54V-DK 는 CMSIS-DAP
  프로브를 보드에 달고 있어서 플래시와 시리얼 콘솔에 케이블 말고는 필요한 게 없다.

![Board Manager 에서 보드가 도는 데까지. URL 하나로 코어·컴파일러·플래시 툴이 깔린다](02-board-manager-flow.png)

이 경로 어디에도 Python 이나 SDK 매니저, `west` 가 없고, 한 번 깔고 나면 오프라인에서도
그대로 된다.

## 발목을 잡는 부분과 그 처리

nRF54L 에서는 페리페럴이 GPIO 포트에 묶여 있다. 아무 핀이나 아무 페리페럴에 붙던
nRF52 와 가장 크게 다른 점이다. PWM 과 ADC 는 P1 에만 닿고, 핀 인터럽트는 P1 과 P0 에는
되지만 P2 에는 절대 안 되며, SPI 는 P2 에서 돌되 신호마다 쓸 수 있는 핀이 둘뿐이다.

포트만 봐서는 부족하다. `PIN_SPI_SCK = P2.03` 은 포트 검사를 통과하고도 동작하지
않는다. `SPIM00.SCK` 는 P2.01 과 P2.06 에만 있기 때문인데, 증상은 "SPI 가 안 된다"
하나뿐이다.

그래서 제약 표를 컴파일 타임에 검사한다. 이 헤더는 손으로 적은 게 아니라 Nordic Pin
Planner 의 SoC 정의에서 생성한다.

`nrf54l/cores/nrf54l/nrf54l_pinmap.h`

```c
#define NRF54L_ASSERT_SIG(pin, sig, what) \
    NRF54L_STATIC_ASSERT(NRF54L_SIG_##sig(pin), what " : " NRF54L_TXT_##sig)

#define NRF54L_SIG_SPIM00_SCK(p)  ((p) == 65 || (p) == 70)
#define NRF54L_TXT_SPIM00_SCK     "SPIM/SPIS00.SCK only works on P2.01, P2.06"
```

[커밋 9e8226a 의 소스](https://github.com/chcbaram/baram-nrf54-arduino/blob/9e8226a7196c20178884d42859b023bdaee9e0ec/nrf54l/cores/nrf54l/nrf54l_pinmap.h#L50-L55)

variant 가 기대하는 배정을 선언해 두면, 보드 정의가 틀렸을 때 물건이 나가는 대신
빌드가 깨진다.

`nrf54l/variants/nu54dk/variant.h`

```c
NRF54L_ASSERT_SIG(PIN_SERIAL_TX, UARTE30_TXD, "Serial(UARTE30) TX");
NRF54L_ASSERT_SIG(PIN_SPI_SCK,   SPIM00_SCK,  "SPI SCK");
```

[커밋 9e8226a 의 소스](https://github.com/chcbaram/baram-nrf54-arduino/blob/9e8226a7196c20178884d42859b023bdaee9e0ec/nrf54l/variants/nu54dk/variant.h#L173-L178)

오류 메시지가 쓸 수 있었던 핀을 알려 주고, 동봉한 PinMap 예제가 칩·보드별 전체 표를
들고 있다.

마이그레이션에서 걸리는 다른 하나는 `analogRead` 다. 내부 기준 전압이 nRF52 의
600 mV 가 아니라 900 mV 고, 1/6 게인도 VDD/4 기준도 없다. `AR_DEFAULT`(3.6 V)와
`AR_INTERNAL_1_8` 은 정확히 맞지만 `AR_INTERNAL_3_0` 은 실제로 3.15 V,
`AR_INTERNAL_2_4` 는 2.25 V, `AR_INTERNAL_1_2` 는 1.35 V 다.
`analogReadMillivolts()` 를 쓰면 이 이야기는 전부 없어진다.

## 이건 아니다

BLE 가 Zephyr/NCS 기반 코어보다 빠르거나 뛰어나지 않다. 그쪽은 Nordic 의 SoftDevice
Controller 를 쓰는데, 여기서 쓰는 SoftDevice 와 같은 인증 컨트롤러 계열이다. 차이는
어떤 API 로 코드를 쓰는가, 설치가 얼마나 무거운가, 프로젝트가 어디로 가는가이지
라디오 품질이 아니다.

Matter, Thread, Zigbee, LE Audio, 802.15.4, MCUboot, TF-M, 파일시스템, 신규 칩의
upstream 지원 — 이런 영역은 Zephyr 가 앞서 있고, 나는 그 영역에서 겨루지 않는다.

솔직하게 적어 두는 장기 리스크는 이것이다. Nordic 은 베어메탈을 nRF5 SDK 사용자의
마이그레이션을 돕고 Zephyr 로 가는 업그레이드 경로를 주는 것으로 포지셔닝한다.
다리로 설계된 제품이라는 뜻이고, 다리는 역할이 끝나면 투자가 줄 수 있다. 이 구조의
가장 큰 리스크이고, 모른 척하는 대신 어떤 조건에서 재검토할지를 문서에 적어 두었다.

## 지금 어디까지

업로드는 아직 `probe-rs` 가 모는 CMSIS-DAP SWD 다. 다음 마일스톤이 UART 와 BLE OTA
DFU 이고, SWD 경로는 그 뒤에도 같이 남긴다 — 부트로더에는 복구 경로가 필요하다.

## 링크

- [baram-nrf54-arduino](https://github.com/chcbaram/baram-nrf54-arduino)
- [지원 범위와 라이브러리별 결과](https://github.com/chcbaram/baram-nrf54-arduino/blob/9e8226a7196c20178884d42859b023bdaee9e0ec/docs/LIBRARY-COMPAT.md)
- [nrfconnect/sdk-nrf-bm](https://github.com/nrfconnect/sdk-nrf-bm)

<!--
sources (commit 9e8226a7196c20178884d42859b023bdaee9e0ec):
- README.ko.md — 왜 만드는가, 특징, 지원 보드, 지원 범위, 구조
- CLAUDE.md — §1 R7/R11/R12, §2 아키텍처, §2.1 왜 베어메탈인가, §2.2 재검토 트리거, §3 업로드 경로
- docs/STATUS.md — tickless 0.0 ppm, 빌드 크기 38004 B / 3856 B, 동시 연결
- nrf54l/cores/nrf54l/nrf54l_pinmap.h, nrf54l/variants/nu54dk/variant.h
- 01-software-stack.png, 02-board-manager-flow.png — 저자가 제공한 구조도
-->
