# 글감 목록

쓸 글을 여기 모아 둔다. 시간 날 때 위에서부터 고른다.

`/write-post <저장소>` 를 주제 없이 실행하면 이 파일을 먼저 본다.
글을 발행하면 그 줄을 **발행됨** 으로 바꾸고 주소를 적는다. 지우지 않는다 — 이력이 된다.

## 저장소 그림 쓰기

저장소에 있는 다이어그램을 최대한 가져다 쓴다. 다만 **라벨이 전부 한국어**다.
영문 글에 넣을 때는 SVG 를 글 폴더에 복사하고 `<text>` 의 라벨만 영어로 바꾼다.
내용은 바꾸지 않는다. 한국어판(`index.ko.md`)은 원본을 그대로 쓴다.

가진 것: **stm32h7-gfx 10장 · titan-mini 7장 · wish-he SVG 6장 + PNG 1장.**
qmk-link · via-he · HG-T113-S3 에는 글에 쓸 다이어그램이 없다 — 새로 그리거나 사진으로 대신한다.

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
| **발행됨** | [Three Sources, Three Different SRAM Sizes](https://chcbaram.github.io/posts/ra8p1-memory-partitions/) | 주소 공간, **SRAM 크기가 세 군데서 다르게 보이는 문제**, MRAM 특성, 파티션을 링커에 알리는 법 | `02-memory-map.md` (1.4k · 7절) · 그림 `memory-map.svg` `mram-layout.svg` `sram-partition.svg` |
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
| **초안** | Putting Hall Effect Under QMK Instead of Forking It | wish-he | matrix 자리에 HE 판정 결과를 넣어 QMK 위 로직을 그대로 두는 방식. 시리즈의 출발점. `content/posts/hall-effect-under-qmk/` (TODO 3, 사진 자리 4) | `README.md` (8.2k) · `10-qmk.md` (1.3k) · 그림 `qmk-he-stack.svg` |
| **초안** | Reading Magnet Depth With an ADC | wish-he | 홀 센서 스캔 구조. 카운트를 얻는 데까지. `content/posts/reading-magnet-depth-with-adc/` (TODO 3, 사진 자리 4, 그림 없음) | `05-adc-scan.md` (1.9k · 6절) · `00-hardware.md` · `12-scan-speed.md` |
| **재료 확인됨** | 자속에서 거리로 — 스위치 곡선 | wish-he | 데이터시트 두 점으로 거리 곡선을 만드는 모델 | `15-distance-curve.md` (2.3k · 13절) · `he-magnet-model.md` (1.8k) |
| **재료 확인됨** | 키가 눌렸다고 판정하기 | wish-he | 입력 지점, 데드존, 보정 | `06-key-decision.md` (1.2k · 7절) · 그림 `keys-pipeline.svg` |
| **발행됨** | [A Ghost Input Above the Actuation Point, and the Two Bugs Under It](https://chcbaram.github.io/posts/wish-he-rapid-trigger/) | wish-he | 되돌린 거리로 떼는 판정. **실제로 겪은 유령 입력 버그가 이슈 문서로 남아 있다.** ⚠ `13-rapid-trigger.md` 는 **버그에 걸리는 절만 썼다**(590 단어). 구현 쪽 1.1k 는 아래 줄로 남아 있다 | `13-rapid-trigger.md` 중 ④·절대 입력지점·연속 RT·RT 가 사는 구간·나가는 쪽 · `issues/002-rapid-trigger-ghost-input.md` · 그림 `issues/images/002-ghost-pulse.svg` |
| **재료 확인됨** | 래피드 트리거를 실제로 구현하기 — 이론 1.73배, 실측 1.31배 | wish-he | 처리를 ADC 변환 대기 안으로 옮긴 것, 3개 이동합과 **이론에 못 미친 잡음 개선을 그대로 기록한 것**, 고치지 않기로 한 드리프트, "이동량은 위치가 아니다" 로 뒤집은 판단 | `13-rapid-trigger.md` 중 안 쓴 절 (①②③ · 바닥 보호와 데드존 · 설정을 전부 키별로 · 뒤에 고친 것 · 배운 것 · 남은 것, 1.1k) · 그림 `issues/images/002-rt-window.svg` |
| **재료 확인됨** | 지연 시간을 실제로 재기 | wish-he | 스캔 주기, HID 동기화, 측정 결과 | `18-latency.md` (1.8k · 9절) · `12-scan-speed.md` (0.8k) · `16-hid-sync.md` (1.0k) · 그림 `issues/images/001-report-gate.svg` |
| **재료 확인됨** | LED 전류 한계와 싸우기 | wish-he | RGB 매트릭스 전류 제한 | `14-led-limiter.md` (3.4k · 13절) |
| **재료 확인됨** | 순정 부트로더 위에 얹기 | wish-he | 보드에 원래 있던 부트로더를 그대로 두고 앱 자리만 쓴다. 언제든 순정 복구 | `01-boot-on-iap.md` (0.5k) · `09-iap-updater.md` (1.1k) |
| **재료 확인됨** | 설정을 어디에 저장하나 | wish-he | 프로파일 4벌, 저장 구조 | `08-storage.md` (1.3k · 10절) |
| **재료 확인됨** | QMK 는 EEPROM 을 원하는데 칩에는 없다 | wish-he | 바이트 단위로 아무 때나 쓸 수 있어야 하는 QMK EEPROM API 를 NOR 플래시 위에 올린 방법. **16KB 를 통째로 RAM 에 들고(그림자), 더러워진 섹터를 200ms 조용할 때 하나씩 굽는다.** SDK 의 `eeprom_emulation` 컴포넌트를 **안 쓴 이유**가 같이 있다. XIP 라 지우는 동안 인터럽트를 막아야 해서 **한 번에 한 섹터만** 굽는다 — 네 섹터를 같이 지우면 USB 리포트가 빠진다(12편 실측) | `11-via.md` §EEPROM 백엔드(225) · §기록은 셋이고 버전도 셋(182) · §프로파일은 둘이 나란히(133) · `08-storage.md` §e2p 컴포넌트를 쓸지(98) · §자리 — 기존 데이터 영역을 피해서(109) · 합 750 |
| **재료 확인됨** | 두 번째 보드로 옮기기 | wish-he | WISH60 에서 WISH61(AE61 Pro)로 | `wish61-he.md` (2.6k · 6절) |
| **재료 확인됨** | 브라우저가 키보드에 직접 붙는다 — WebHID VIA 포크 | via-he | VIA 포크에 HE 전용 기능을 더한 것. 설치 없이 크롬에서 설정하고 펌웨어까지 굽는다 | via-he `README.md` · wish-he `11-via.md` (3.0k · 11절) · 화면 `images/via-he-settings.png` |
| **재료 확인됨** | HPM5361 개발 환경과 벤더 SDK 를 들여온 구조 | wish-he | **`hpm_sdk` 에 의존하지 않는다.** 필요한 SoC 헤더·드라이버·링커 스크립트만 `src/lib/hpm_sdk/`(306 파일)와 `src/bsp/`(device · ldscript 3종)로 들여왔고 CMake 는 `set(HPM_SDK_DIR src/lib/hpm_sdk)` 한 줄이다. 그래서 준비할 것이 컴파일러뿐이다. 툴체인은 xPack RISC-V GCC, `tools/hpmicro-riscv-gcc.cmake` 가 xPack·HPMicro **두 접두어를 다 안다**. **OpenOCD 는 HPMicro 배포판이어야 한다** — homebrew 판에는 `hpm_xpi` 가 없어 굽지 못하고 읽기·디버깅까지만 된다. pip 패키지도 안 쓴다(업데이터가 ctypes 로 libhidapi 직접). 프로브 함정: 클론 J-Link 은 SEGGER DLL 이 `0xFFFFFEFA` 로 거부하고, **펌웨어 업데이트를 수락하면 벽돌**이 된다. 계층(`ap`/`hw`/`bsp`/`common`/`lib`)은 titan-mini 와 같아서 **그 글의 계층 규칙과 이어진다** | `docs/README.md` §1 개발 환경 · §2 빌드 (1.0k) · `CMakeLists.txt`(458줄) · `tools/hpmicro-riscv-gcc.cmake` · `src/lib/hpm_sdk/` · `src/bsp/ldscript/` · 저장소 `CLAUDE.md` §굽기 |
| **확인 필요** | 무엇을 어떻게 검증했나 | wish-he | 검증 절차 전반. **6.3k 단어라 한 편에 안 들어간다 — 쪼갤 각도를 먼저 정한다** | `17-verification.md` (6.3k) · `checklist.md` (2.1k) |

> 쓰는 순서는 위에서부터가 자연스럽다. 컨셉 → 읽기(ADC) → 거리 → 판정 → 래피드 트리거
> 순으로 가야 뒤 글이 앞 글을 전제할 수 있다.
>
> ⚠ **이동합(3개 표본 합)은 RT 구현 글 몫이다.** `05-adc-scan.md` 도 그 이야기를
> 직접 하지 않고 "13편에서 3개 이동합을 넣었다" 로 넘긴다. ADC 글에서 끌어다 쓰지 않는다.
>
> `00-hardware.md`(1.4k), `02-console.md`, `03-reset-boot.md`, `04-ws2812.md`, `07-keyboard.md` 는
> 단독으로 쓰기에 얇다. 관련 글의 도입부로 녹인다.
>
> ⚠ **EEPROM 글의 경계.** QMK 글 초안이 RAM 그림자와 200ms 미룬 굽기를 **한 문단으로
> 요약해** 두었다(`hall-effect-under-qmk/index.md`). EEPROM 글은 그 문단을 되풀이하지
> 말고 그 아래를 판다 — 플래시 배치, SDK 컴포넌트를 안 쓴 판단, 16KB 의 속(EECONFIG /
> 사용자 512B / 키맵 1024B x 4 / 매크로 11735B), 기록 셋과 버전 셋, 프로파일 둘.
> "설정을 어디에 저장하나"(`08-storage.md`) 줄과도 갈린다 — 그쪽은 **HE 자체 설정의
> 플래시 핑퐁**이고, 이 글은 **QMK/VIA 용 EEPROM** 이다. 플래시 배치도만 공유한다.

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

## stm32h7-gfx — SWD 오프라인 다운로더

시리즈 **`SWD Downloader`**. PC 도 ST-LINK 도 없이 보드 하나로 다른 MCU 에 펌웨어를
굽는 장비다. STM32H723(550 MHz, 480×480 터치 LCD, LVGL)이 SD 카드에서 펌웨어를 골라
타깃에 쓰고 검증한다. 배선은 **SWCLK = PE3, SWDIO = PC10 둘뿐**이다.

저장소의 `firmware/stm32h7-lvgl/docs/` 가 이미 13편짜리 연재로 정리돼 있고 각 편에
제목까지 붙어 있다. **그림도 SVG 10장**으로 갖춰져 있다 (`docs/images/`).
아래는 글 길이에 맞춰 묶은 것이다.

| 상태 | 제목 (가제) | 무엇을 다루나 | 근거 |
| --- | --- | --- | --- |
| **재료 확인됨** | 선 두 가닥으로 남의 MCU 와 대화하기 | SWD 프로토콜, GPIO 비트뱅잉, turnaround, MODER 캐싱, **내장 로직 애널라이저로 간헐 비트 오류를 잡은 이야기** | `01-swd-transport.md` (1.3k · 4절) · 그림 `swd-layers.svg` `swd-transaction.svg` |
| **재료 확인됨** | 타깃 메모리를 읽고, 코어를 세우고, 내 코드를 돌리기 | ADIv5 DP/AP, MEM-AP, posted read 와 1 KB TAR 랩 함정, halt/run/step, 함수 호출 규약을 SWD 로 흉내내기 | `02-dap-memory.md` (0.4k) + `03-debug-core.md` (0.3k) + `04-algo-runner.md` (0.5k) — **셋을 묶어야 한 편이 된다** |
| **재료 확인됨** | 플래시 알고리즘을 어디서 구하나 | CMSIS-Pack `.FLM` 포맷, 검증, SD 카드 배치 | `05-flash-algorithm.md` (1.1k · 6절) · 그림 `flm-layout.svg` `algo-layer.svg` |
| **재료 확인됨** | ELF 파서를 펌웨어에 넣기 | 스트리밍 ELF32 파서, 재배치, 타깃 RAM 로드 | `06-elf-loader.md` (0.8k · 6절) |
| **재료 확인됨** | 첫 굽기 — 그리고 타깃을 한 번 죽였다 | `FlashDevice` 바인딩, 파일 굽기, **링크를 잃고 복구한 과정** | `07-first-burn.md` (1.0k · 7절) |
| **재료 확인됨** | 얼마나 빠른가 | pyOCD · ST 도구와 비교, 이중 버퍼링, 병목 분석 | `08-performance.md` (0.9k · 8절) · 그림 `double-buffer.svg` |
| **재료 확인됨** | 펌웨어 파일 세 가지 | `.bin` / `.elf` / Intel HEX, 주소는 어디서 오나 | `09-image-format.md` (1.1k · 7절) · 그림 `image-format.svg` |
| **재료 확인됨** | ST 로더를 빌려 쓰다 | `.stldr` 지원, 알고리즘 계층 분리, **ST 도구보다 빨라진 지점** | `10-stldr.md` (1.1k · 9절) |
| **재료 확인됨** | 인자 네 개를 하나로 — 디바이스 DB | 자동 판별, `fw.txt` 잡 | `11-device-db.md` (1.2k · 9절) · 그림 `device-db.svg` |
| **재료 확인됨** | 외부 QSPI 에 굽기 | AP 선택, DPv2 TARGETID, 외부 로더, MPU 사건 | `12-external-loader.md` (1.5k · 9절) · 그림 `external-loader.svg` |
| **확인 필요** | 화면을 붙이다 | LVGL 앱, 워커 분리, **손으로 만져야만 보이는 버그 11개**. 2.1k 라 쪼갤 각도를 먼저 정한다 | `13-gui.md` (2.1k · 9절) · 그림 `gui-pages.svg` |

> 이 시리즈의 첫 글은 **1편**이 맞다. "ARM 표준이라 벤더가 바뀌어도 같은 코드가 돈다"
> 는 계층 이야기가 시리즈 전체의 전제라서, 그걸 먼저 세워 두면 뒤 글이 짧아진다.
>
> ⚠ 로컬 클론이 origin 보다 뒤처져 있었다(2026-09-27 확인). 쓰기 전에 `git fetch` 하고
> `git show origin/main:<path>` 로 읽는다.

## HG-T113-S3

Allwinner T113-S3 보드(HiGenis HG-T113-S3-KIT)의 펌웨어 전부. U-Boot · 리눅스 커널 ·
rootfs 를 빌드해 SPI NOR 에 굽고, 그 위에서 LVGL 앱을 돌린다. 호스트에 필요한 것은
**docker 하나**이고, 보드와 PC 는 **USB-C 한 가닥**으로 FEL · fastboot · USB 네트워크를
전부 쓴다.

문서가 README 세 개뿐이라 글감이 굵게 잡힌다. 그림은 스플래시 로고 하나뿐이니
사진이나 새로 그린 그림이 필요하다.

| 상태 | 제목 (가제) | 무엇을 다루나 | 근거 |
| --- | --- | --- | --- |
| **확인 필요** | docker 하나로 리눅스 보드 전체를 빌드하기 | 크로스 컴파일러·커널 의존성을 전부 컨테이너에 넣은 구성. `sudo` 로 돌리면 안 되는 이유까지 | `sdk/README.md` (3.7k) — **분량이 커서 두 편으로 나눌 것** |
| **확인 필요** | USB-C 한 가닥으로 FEL · fastboot · 네트워크까지 | J10 포트 하나로 굽고 붙는 흐름 | `README.md` (1.0k) · `sdk/README.md` |
| **확인 필요** | MCU 펌웨어 구조를 리눅스 앱에 그대로 옮기기 | `stm32h7-lvgl` 과 같은 `ap` / `hw` 계층을 쓰고 `hw/driver` 만 갈아끼웠다. **titan-mini 글의 계층 규칙과 이어지는 주제** | `app/README.md` (1.6k) |

## baram-term

저장소에 `docs/` 가 갖춰져 있다 — `decisions.md` (3.8k) 가 설계 결정의 정본이고
`architecture.md` (0.8k), `roadmap.md` (2.1k) 가 있다. 그림은 `docs/images/architecture.png`
하나이고 생성 스크립트(`make_architecture.py`)가 같이 있다.

| 상태 | 제목 (가제) | 무엇을 다루나 | 근거 |
| --- | --- | --- | --- |
| **재료 확인됨** | 선을 뽑고 BLE 로 갈아타기 — 터미널 하나도 안 고치고 | Nordic UART Service 를 `ble://이름` 포트로 붙인 이야기. **터미널·그래프·HEX·로그·자동완성·외부 제어가 하나도 안 바뀐 이유**는 장치 객체가 pyserial 의 최소 면(`read`/`write`/`in_waiting`/`close`/`is_open`)만 요구하도록 seam 을 잡아 뒀기 때문이다 (`fake_device.py` 와 같은 면) | `docs/ble.md` (0.7k · 6절) · `src/baram_term/ble.py` (285줄, 머리말 주석이 설계 근거를 담고 있다) · README 의 "BLE 보드에 붙기" |
| **확인 필요** | 시리얼 터미널 안에 진짜 픽셀 그래프 그리기 | 글자 격자 TUI 처럼 보이지만 실제로는 GUI 창. Teleplot / Arduino 플로터 형식 자동 인식 | README, `retro-ui/`, `docs/architecture.md` |
| **확인 필요** | 보드를 뽑았다 꽂아도 부팅 로그를 놓치지 않기 | 자동 재연결 | README |
| **확인 필요** | `help` 출력에서 명령을 배우는 Tab 자동완성 | 포트별로 명령 목록을 기억하는 방식 | README, `completion.py` |
| **확인 필요** | Claude Code 가 보드 CLI 를 두드리게 하기 | `baram-term ctl` 외부 제어. 포트를 넘겨주지 않고 오간 내용이 화면에 그대로 보인다 | `docs/external-control.md` (0.8k · 6절) |

> ### BLE 글에 꼭 넣을 것 — 저장소에 근거가 있는 판단 세 가지
>
> 1. **주소가 아니라 이름을 저장한다.** macOS 는 장치 주소 대신 PC 마다 다른
>    CoreBluetooth UUID 를 주기 때문에, 주소로 저장하면 다른 PC 에서 같은 보드를
>    못 찾는다. 같은 이름이 여럿이면 광고의 제조사 데이터 끝 4바이트를 꼬리표로
>    붙인다 (`ble://이름#1a2b3c4d`).
> 2. **bleak 을 함수 안에서 늦게 불러온다.** 선택 설치라 없는 PC 에서도 baram-term 이
>    떠야 하고, BLE 를 안 쓰는 사람이 macOS 블루투스 권한 대화상자를 볼 이유가 없다.
> 3. **asyncio 를 앱까지 끌고 오지 않는다.** bleak 은 asyncio 전용이라 장치마다
>    백그라운드 스레드에서 이벤트 루프를 돌리고, 앱의 수신·송신 스레드는 평소처럼
>    블로킹 호출만 한다.
>
> 비공개 규칙 문서 `docs/device-testing.md` 를 먼저 읽고 따른다.

## 아직 정하지 않은 것

- `content/projects/via-he/_index.md` — via-he 첫 글 쓸 때 같이 만든다
  (`wish-he` 는 2026-09-27 에 만들었다)
- 한국어판은 **발행하는 글마다 같이 만든다** (2026-09-27 결정). 발행된 글 5편과
  프로젝트 페이지 4개는 `index.ko.md` / `_index.ko.md` 가 다 있다. 새 글을 쓸 때
  한국어판을 같이 만들지 않으면 `/ko/` 쪽이 빈다
