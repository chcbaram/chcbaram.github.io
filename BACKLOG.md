# 글감 목록

쓸 글을 여기 모아 둔다. 시간 날 때 위에서부터 고른다.

`/write-post <저장소>` 를 주제 없이 실행하면 이 파일을 먼저 본다.
글을 발행하면 그 줄을 **발행됨** 으로 바꾸고 주소를 적는다. 지우지 않는다 — 이력이 된다.

## 상태

| 상태 | 뜻 |
| --- | --- |
| **발행됨** | 사이트에 올라가 있다 |
| **초안** | `content/posts/` 에 draft 로 있다. TODO 나 사진이 남았다 |
| **재료 확인됨** | 저장소에 근거 문서가 있고 분량도 확인했다. 바로 쓸 수 있다 |
| **확인 필요** | 쓸 만해 보이지만 저장소에서 근거를 아직 확인하지 않았다 |
| **대기** | 구현이 아직 안 끝났다. 끝난 뒤에 쓴다 |

---

## titan-mini (RA8P1)

시리즈 `Titan Mini (RA8P1)` 로 묶는다. 저장소의 `firmware/docs/` 가 재료다.

| 상태 | 제목 (가제) | 무엇을 다루나 | 근거 |
| --- | --- | --- | --- |
| **초안** | Laying Out a Dual-Core Firmware Project, and Proving It With One LED | 디렉터리 배치, `ap` 는 벤더 HAL 을 모른다는 계층 규칙, 검사기, 첫 LED | `12-project-skeleton.md` (1.4k) · `20-led.md` |
| **초안** | Waking the Second Core Is Easy. Knowing It Woke Is Not. | FSP 멀티코어 API 하나, 공유 블록 핸드셰이크, 낡은 magic 함정, pyOCD/DFP 함정 | `23-cm33-boot.md` (2.1k) · `04-dualcore.md` |
| **재료 확인됨** | 단일 뱅크 MRAM 과 1872 KB SRAM 을 두 코어에 나누기 | 주소 공간, **SRAM 크기가 세 군데서 다르게 보이는 문제**, MRAM 특성, 파티션을 링커에 알리는 법 | `02-memory-map.md` (1.4k · 7절) |
| **재료 확인됨** | FreeRTOS, 모듈 자동 등록, 이벤트 버스 | `.module` 섹션으로 모듈을 자동 등록하는 방식과 이벤트 버스 | `22-freertos.md` (2.4k · 13절) — 분량이 커서 두 편으로 나눌 수도 |
| **재료 확인됨** | UART 와 CLI 를 올리기 | SCI2 콘솔, CLI 구조 | `21-uart-cli.md` (1.4k · 7절) |
| **확인 필요** | 세 OS 에서 같은 빌드 유지하기 | 툴체인, CMake, pyOCD 를 Windows/Linux/macOS 에서 굴리기 | `13-os-setup.md` (1.6k) · `11-fsp-config.md` (0.9k) |
| **대기** | 부트로더 설계 — FSBL 없는 2단 구조 | 이미지 컨테이너, 업데이트 흐름, ITCM 실행 | `05-boot-architecture.md` (1.4k) — **설계만 됨. 구현은 40번, ITCM 재배치 실측은 25번** |

> `01-boot-sequence.md` (0.9k) 는 단독으로 쓰지 않는다. 절반이 다른 글과 겹치므로
> 메모리 글이나 CM33 글의 도입부로 녹인다.

## baram-nrf54-arduino

시리즈 `nRF54L Arduino Core`.

| 상태 | 제목 (가제) | 무엇을 다루나 | 근거 |
| --- | --- | --- | --- |
| **발행됨** | An Arduino Core for the nRF54L, Built for Bluefruit Compatibility | 왜 만들었나, 계층 구조, 얻는 것과 잃는 것 | `/posts/arduino-core-for-the-nrf54l/` |
| **확인 필요** | nRF52 Bluefruit 스케치를 nRF54L 로 옮기기 | 그대로 되는 것과 달라지는 것. 포트 고정 핀 제약, `analogRead` 기준 전압 차이 | README 의 Support scope, `docs/EXAMPLE-COMPAT.md`, `docs/LIBRARY-COMPAT.md` |
| **확인 필요** | FreeRTOS 위에서 Bluefruit 의 `delay()` 와 `Scheduler.startLoop()` 맞추기 | 호환을 위해 스케줄러 동작을 어떻게 맞췄는지 | 코어 소스와 커밋 이력 |
| **확인 필요** | 0.1.0 에서 0.4.0 까지 | 릴리스별로 무엇이 추가됐는지 | `gh release list`, 커밋 이력 |

## baram-term

| 상태 | 제목 (가제) | 무엇을 다루나 | 근거 |
| --- | --- | --- | --- |
| **확인 필요** | 시리얼 터미널 안에 진짜 픽셀 그래프 그리기 | 글자 격자 TUI 처럼 보이지만 실제로는 GUI 창. Teleplot / Arduino 플로터 형식 자동 인식 | README, `retro-ui/` |
| **확인 필요** | 보드를 뽑았다 꽂아도 부팅 로그를 놓치지 않기 | 자동 재연결 | README |
| **확인 필요** | `help` 출력에서 명령을 배우는 Tab 자동완성 | 포트별로 명령 목록을 기억하는 방식 | README |

> 비공개 규칙 문서 `docs/device-testing.md` 를 먼저 읽고 따른다.

## 아직 정하지 않은 것

- qmk-link, wish-he, via-he — 프로젝트 페이지부터 만들지 정한다
- 한국어판을 붙일 글 고르기. 지금은 nRF54L 글만 `index.ko.md` 가 있다
