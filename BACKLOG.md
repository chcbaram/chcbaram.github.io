# 글감 목록

쓸 글을 여기 모아 둔다. 시간 날 때 위에서부터 고른다.

`/write-post <저장소>` 를 주제 없이 실행하면 이 파일을 먼저 본다.
글을 발행하면 그 줄을 **발행됨** 으로 바꾸고 주소를 적는다. 지우지 않는다 — 이력이 된다.

## 저장소 그림 쓰기

저장소에 있는 다이어그램을 최대한 가져다 쓴다. 다만 **라벨이 전부 한국어**다.
영문 글에 넣을 때는 SVG 를 글 폴더에 복사하고 `<text>` 의 라벨만 영어로 바꾼다.
내용은 바꾸지 않는다. 한국어판(`index.ko.md`)은 원본을 그대로 쓴다.

가진 것: **titan-mini 7장 · wish-he SVG 6장 + PNG 1장.** qmk-link 와 via-he 에는
글에 쓸 다이어그램이 없다 — 필요하면 새로 그리거나 사진으로 대신한다.

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
| **발행됨** | [Laying Out a Dual-Core Firmware Project, and Proving It With One LED](https://chcbaram.github.io/posts/titan-mini-firmware-skeleton/) | 디렉터리 배치, `ap` 는 벤더 HAL 을 모른다는 계층 규칙, 검사기, 첫 LED | `12-project-skeleton.md` (1.4k) · `20-led.md` |
| **발행됨** | [Waking the Second Core Is Easy. Knowing It Woke Is Not.](https://chcbaram.github.io/posts/waking-the-second-core/) | FSP 멀티코어 API 하나, 공유 블록 핸드셰이크, 낡은 magic 함정, pyOCD/DFP 함정 | `23-cm33-boot.md` (2.1k) · `04-dualcore.md` · `images/dualcore-start.svg` (고쳐서 옮겨 그림, 아래 메모) |
| **재료 확인됨** | 단일 뱅크 MRAM 과 1872 KB SRAM 을 두 코어에 나누기 | 주소 공간, **SRAM 크기가 세 군데서 다르게 보이는 문제**, MRAM 특성, 파티션을 링커에 알리는 법 | `02-memory-map.md` (1.4k · 7절) · 그림 `memory-map.svg` `mram-layout.svg` `sram-partition.svg` |
| **재료 확인됨** | FreeRTOS, 모듈 자동 등록, 이벤트 버스 | `.module` 섹션으로 모듈을 자동 등록하는 방식과 이벤트 버스 | `22-freertos.md` (2.4k · 13절) — 분량이 커서 두 편으로 나눌 수도 |
| **재료 확인됨** | UART 와 CLI 를 올리기 | SCI2 콘솔, CLI 구조 | `21-uart-cli.md` (1.4k · 7절) |
| **확인 필요** | 세 OS 에서 같은 빌드 유지하기 | 툴체인, CMake, pyOCD 를 Windows/Linux/macOS 에서 굴리기 | `13-os-setup.md` (1.6k) · `11-fsp-config.md` (0.9k) |
| **대기** | 부트로더 설계 — FSBL 없는 2단 구조 | 이미지 컨테이너, 업데이트 흐름, ITCM 실행 | `05-boot-architecture.md` (1.4k) · 그림 `fw-image-format.svg` `update-flow.svg` — **설계만 됨. 구현은 40번, ITCM 재배치 실측은 25번** |

> ⚠ **`images/dualcore-start.svg` 는 코드와 다르다.** 그림은 ⑥⑦ 단계를
> `R_BSP_IpcSemaphoreTake/Give` 로 기동을 확인하는 것으로 그려 두었는데, 실제
> `hw/driver/ipc.c` 는 세마포어를 쓰지 않고 공유 블록 magic 핸드셰이크를 쓴다
> (`shared.magic = 0` → `R_BSP_SecondaryCoreStart()` → magic 대기).
> `04-dualcore.md` 가 이 그림을 참조한다. 글에는 ⑥⑦ 을 코드에 맞게 고치고 라벨을
> 영어로 바꾼 사본을 넣었다(`content/posts/waking-the-second-core/dualcore-start.svg`).
> **저장소 쪽 원본도 고쳐야 한다.**
>
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

## WISH HE — wish-he (펌웨어) + via-he (설정 도구)

두 저장소가 한 제품이다. 시리즈는 **`WISH HE`** 하나로 묶고, `projects` 로 어느 저장소
이야기인지 나눈다. 상용 홀이펙트 키보드(Geonworks VENOM60HE 7U / EverGlide AE61 Pro)에
올리는 커스텀 펌웨어와, 그것을 브라우저에서 설정하는 VIA 포크다.

핵심 컨셉 한 줄: **QMK 를 바꾸지 않는다.** 키 판정만 홀이펙트로 바꿔 끼워서
레이어·매크로·탭홀드와 VIA 설정을 하나도 잃지 않는다.

> ⚠ `via-he` 는 이미 `chcbaram.github.io/via-he/` 에 프로젝트 페이지로 떠 있다.
> 블로그 저장소의 `content/` 최상위나 `static/` 에 `via-he` 라는 이름을 만들지 않는다.

| 상태 | 제목 (가제) | 저장소 | 무엇을 다루나 | 근거 |
| --- | --- | --- | --- | --- |
| **재료 확인됨** | QMK 를 바꾸지 않고 그 아래에 홀이펙트를 끼우기 | wish-he | matrix 자리에 HE 판정 결과를 넣어 QMK 위 로직을 그대로 두는 방식. 시리즈의 출발점 | `README.md` (8.2k) · `10-qmk.md` (1.3k) · 그림 `qmk-he-stack.svg` |
| **재료 확인됨** | 자석 위치를 전압으로 읽기 — ADC 스캔 | wish-he | 홀 센서 스캔 구조 | `05-adc-scan.md` (1.9k · 6절) |
| **재료 확인됨** | 자속에서 거리로 — 스위치 곡선 | wish-he | 데이터시트 두 점으로 거리 곡선을 만드는 모델 | `15-distance-curve.md` (2.3k · 13절) · `he-magnet-model.md` (1.8k) |
| **재료 확인됨** | 키가 눌렸다고 판정하기 | wish-he | 입력 지점, 데드존, 보정 | `06-key-decision.md` (1.2k · 7절) · 그림 `keys-pipeline.svg` |
| **재료 확인됨** | 래피드 트리거와 유령 입력 | wish-he | 되돌린 거리로 떼는 판정. **실제로 겪은 유령 입력 버그가 이슈 문서로 남아 있다** | `13-rapid-trigger.md` (2.1k · 11절) · `issues/002-rapid-trigger-ghost-input.md` · 그림 `issues/images/002-ghost-pulse.svg` `002-rt-window.svg` |
| **재료 확인됨** | 지연 시간을 실제로 재기 | wish-he | 스캔 주기, HID 동기화, 측정 결과 | `18-latency.md` (1.8k · 9절) · `12-scan-speed.md` (0.8k) · `16-hid-sync.md` (1.0k) · 그림 `issues/images/001-report-gate.svg` |
| **재료 확인됨** | LED 전류 한계와 싸우기 | wish-he | RGB 매트릭스 전류 제한 | `14-led-limiter.md` (3.4k · 13절) |
| **재료 확인됨** | 순정 부트로더 위에 얹기 | wish-he | 보드에 원래 있던 부트로더를 그대로 두고 앱 자리만 쓴다. 언제든 순정 복구 | `01-boot-on-iap.md` (0.5k) · `09-iap-updater.md` (1.1k) |
| **재료 확인됨** | 설정을 어디에 저장하나 | wish-he | 프로파일 4벌, 저장 구조 | `08-storage.md` (1.3k · 10절) |
| **재료 확인됨** | 두 번째 보드로 옮기기 | wish-he | WISH60 에서 WISH61(AE61 Pro)로 | `wish61-he.md` (2.6k · 6절) |
| **재료 확인됨** | 브라우저가 키보드에 직접 붙는다 — WebHID VIA 포크 | via-he | VIA 포크에 HE 전용 기능을 더한 것. 설치 없이 크롬에서 설정하고 펌웨어까지 굽는다 | via-he `README.md` · wish-he `11-via.md` (3.0k · 11절) · 화면 `images/via-he-settings.png` |
| **확인 필요** | 무엇을 어떻게 검증했나 | wish-he | 검증 절차 전반. **6.3k 단어라 한 편에 안 들어간다 — 쪼갤 각도를 먼저 정한다** | `17-verification.md` (6.3k) · `checklist.md` (2.1k) |

> 쓰는 순서는 위에서부터가 자연스럽다. 컨셉 → 읽기(ADC) → 거리 → 판정 → 래피드 트리거
> 순으로 가야 뒤 글이 앞 글을 전제할 수 있다.
>
> `00-hardware.md`(1.4k), `02-console.md`, `03-reset-boot.md`, `04-ws2812.md`, `07-keyboard.md` 는
> 단독으로 쓰기에 얇다. 관련 글의 도입부로 녹인다.

## qmk-link

시리즈 **`qmk-link`**. 일반 USB 키보드를 QMK / VIA / Vial 키보드로 바꿔 주는 어댑터다.
RP2350A 위에서 PIO USB 호스트로 키보드를 받아 QMK 를 태우고, PC 에는 편집 가능한
키보드로 보이게 한다.

> ⚠ `qmk-link` 는 이미 `chcbaram.github.io/qmk-link/` 에 배열 마법사가 떠 있다.
> 블로그 저장소에 같은 이름의 경로를 만들지 않는다.
>
> 이 저장소에는 **그림이 하나도 없다.** 보드 사진과 동작 사진으로 채우거나,
> 필요하면 다이어그램을 새로 그린다. 회로도는 `hardware/RP2350-USB-A.pdf` 에 있다.

| 상태 | 제목 (가제) | 무엇을 다루나 | 근거 |
| --- | --- | --- | --- |
| **재료 확인됨** | 아무 USB 키보드나 QMK 키보드로 바꾸기 | 왜 만들었나, USB-A 로 받아 Type-C 로 내보내는 구조 | `00-context.md` (4.9k · 15절) — 분량이 커서 **두 편으로 나눌 것** · `README.md` |
| **재료 확인됨** | RP2350 에서 USB 호스트와 디바이스를 동시에 | PIO USB 호스트(GPIO12/13), 네이티브 USB 디바이스, 120 MHz 제약 | `03-usb-host.md` (0.9k) · `04-usb-device-hid.md` (0.9k) · `usb-stack.md` (0.7k) · `hardware.md` (1.3k) |
| **재료 확인됨** | 받은 키를 QMK 에 먹이기 | 호스트로 읽은 HID 리포트를 QMK matrix 로 넣는 방식 | `05-qmk.md` (1.3k · 8절) |
| **재료 확인됨** | VIA 와 Vial 을 둘 다 지원하기 | 두 프로토콜의 차이와 붙이는 법 | `06-via.md` (2.8k · 7절) · `07-vial.md` (2.3k · 6절) |
| **재료 확인됨** | 꽂힌 키보드의 배열을 알아내기 — 배열 마법사 | 키보드마다 다른 배열을 브라우저에서 만들어 넣는 방식 | `09-keyboard-profile.md` (4.3k · 6절) · `web/` |
| **확인 필요** | Vial 앱에서 매크로와 탭댄스가 안 보이던 문제 | 이슈 하나를 끝까지 따라간 글 | `issues/001-vial-app-macro-tapdance.md` |

> `01-led.md`, `02-cli-cdc.md`, `08-finalize.md`, `setup-*.md` 는 단독으로 쓰기에 얇거나
> 설치 안내라서 글감이 아니다. `roadmap.md` (0.7k) 는 앞으로 할 것이므로 글의 마지막 절 재료다.

## baram-term

| 상태 | 제목 (가제) | 무엇을 다루나 | 근거 |
| --- | --- | --- | --- |
| **확인 필요** | 시리얼 터미널 안에 진짜 픽셀 그래프 그리기 | 글자 격자 TUI 처럼 보이지만 실제로는 GUI 창. Teleplot / Arduino 플로터 형식 자동 인식 | README, `retro-ui/` |
| **확인 필요** | 보드를 뽑았다 꽂아도 부팅 로그를 놓치지 않기 | 자동 재연결 | README |
| **확인 필요** | `help` 출력에서 명령을 배우는 Tab 자동완성 | 포트별로 명령 목록을 기억하는 방식 | README |

> 비공개 규칙 문서 `docs/device-testing.md` 를 먼저 읽고 따른다.

## 아직 정하지 않은 것

- `content/projects/wish-he/_index.md` 와 `via-he/_index.md` — 첫 글 쓸 때 같이 만든다
- 한국어판을 붙일 글 고르기. 지금은 nRF54L 글만 `index.ko.md` 가 있다
