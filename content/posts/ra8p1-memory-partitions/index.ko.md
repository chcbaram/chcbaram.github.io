---
title: "출처 셋, SRAM 크기 셋"
date: 2026-09-27T03:58:04+09:00
description: "RA8P1 의 SRAM 이 얼마인지를 두고 디바이스 팩과 데이터시트와 생성된 링커 스크립트가 서로 다른 말을 한다. 그것을 정리한 이야기와, 부트로더가 어디서 돌아야 하는지를 결정해 버린 MRAM 제약."
projects: ["titan-mini"]
tags: ["ra8p1", "renesas", "memory", "linker", "mram", "firmware"]
series: ["Titan Mini (RA8P1)"]
repo: "https://github.com/chcbaram/titan-mini"
image: "mram-layout.svg"
ai_assisted: true
naver_url: ""
draft: false
---

Titan Mini 보드에서 메모리를 두 코어로 나누기 전에 답이 필요한 질문이 둘 있었다.
`R7KA8P1KFLCAC` 의 SRAM 은 실제로 얼마인가? 그리고 MRAM 에서 코드를 실행하면서
그 MRAM 에 쓸 수 있는가?

둘 다 예상한 곳에 답이 없었다.

## 출처 셋, 크기 셋

| 출처 | 값 |
|---|---|
| DFP 디바이스 팩 | `0x1A_0000` — 1664 KB |
| 데이터시트 | "1664 KB user SRAM" |
| 생성된 링커 스크립트 | `0x1D_4000` — **1872 KB** |

208 KB 차이다. 반올림으로 생긴 차이가 아니다. 혼자 다른 말을 하는 건 생성된 링커
스크립트인데, 맞는 것도 그쪽이다.

하드웨어 매뉴얼의 메모리 맵이 정리해 준다.

```
0x2200_0000 ~ 0x2219_FFFF   S0BI/S1BI/S2BI/S3BI   1664 KB
0x221A_0000 ~ 0x221D_3FFF   S0BI/S1BI/S2BI/S3BI    208 KB
```

두 항목이 이어져 있고 사이에 구멍이 없다. 합치면 `0x1D_4000`, 1872 KB 다. 디바이스
팩과 데이터시트는 첫 블록까지만 세고 만 것이다.

그래서 링커에는 `0x1D_4000` 을 준다. 데이터시트를 믿었으면 CPU1 에 배정한 양보다도
많은 208 KB 가 쓰이지도 보이지도 않은 채 남았을 것이다.

## MRAM 은 뱅크가 하나고, 그게 많은 걸 결정한다

RA8P1 은 코드 저장에 플래시가 아니라 MRAM 을 쓴다. 성질은 대체로 편한 쪽이다.
FSP 가 모는 기준으로 프로그래밍 단위가 32 바이트고, ECC 가 2비트 오류를 고치고
3비트 오류를 잡아내며, 지우기 단계가 없다.

편하지 않은 성질이 하나 있다. 매뉴얼의 병렬 접근 항목에서 가져오면 이렇다.

- 백그라운드 동작은 **서로 다른 MRAM 뱅크 사이에서만** 된다.
- 같은 매크로에 대한 읽기와 프로그램은 중재되고, 절대 동시에 돌지 않는다.
- 프로그래밍 중에는 인터럽트나 예외가 코드 MRAM 에서 벡터를 가져오지 못한다.

RA8P1 의 뱅크는 정확히 하나다. 그래서 백그라운드 동작은 아예 못 쓰고, MRAM 에서
실행하면서 MRAM 에 쓰는 것은 권장하지 않는 정도가 아니라 성립하지 않는다.
프로그래밍이 끝날 때까지 명령어 인출이 막히는데, 그 프로그래밍이 끝나기를 기다리는
폴링 루프가 바로 자기 다음 명령어를 못 가져오기 때문이다.

**MRAM 에 쓰는 코드는 전부 RAM 에서 돌아야 한다.** 부트로더 입장에서 이건 나중에
처리할 세부가 아니라 물건의 모양 그 자체다. 본체는 통째로 ITCM 으로 옮기고, MRAM 에는
벡터와 스타트업 코드와 복사 테이블만 남는다.

![MRAM 파티션 계획. 부트로더 본체는 ITCM 으로 재배치된다](mram-layout.svg)

## 링커가 이미 할 줄 안다

자기 자신을 복사하는 부트 스텁을 짜야 할 줄 알았다. 그런데 FSP 가 생성해 주는 링커
스크립트에 MRAM 에서 로드해 RAM 에서 실행하는 섹션이 이미 정의돼 있었다.

`src/lib/ra_sdk/cm85/fsp_gen.ld`

```
__itcm_from_flash$$ : { *(.itcm_from_flash) *(.itcm_code_from_flash) } > ITCM AT > FLASH
__dtcm_from_flash$$ : { *(.dtcm_from_flash) *(.dtcm_code_from_flash) } > DTCM AT > FLASH
__ram_from_flash$$  : { *(.ram_from_flash)  *(.ram_code_from_flash)  } > RAM  AT > FLASH
```

[커밋 e0b0dcf 의 소스](https://github.com/chcbaram/titan-mini/blob/e0b0dcf1cc8f503b62323c9668f18656d4df1211/firmware/ra8p1-fw/src/lib/ra_sdk/cm85/fsp_gen.ld)

`$$Base` / `$$Limit` / `$$Load` 심볼이 BSP 의 복사 테이블에 들어가고,
`SystemRuntimeInit()` 이 `SystemInit()` 안에서, `main()` 전에 복사를 수행한다.
`.data` 를 초기화하는 것과 같은 장치다.

그래서 전체가 소스에 붙이는 속성 하나로 줄어든다.

```c
#define BOOT_CODE   __attribute__((section(".itcm_code_from_flash")))
```

남은 MRAM 규칙은 흔한 것들이다. 프로그래밍 중에 주파수를 바꾸거나 스탠바이로 가지
않을 것, 쓰기 뒤에 배리어와 플러시와 완료 대기를 둘 것. 그 대기에서 CPU 를 세우지
않으려면 더미 읽기 대신 `MRCPS.PRGBSYC` 를 폴링한다.

## 파티션 계획

부트로더가 생기면 MRAM 은 세 영역이 된다. 지금은 CPU0 펌웨어가 전부 쓰고 있다.

| 영역 | 시작 | 크기 |
|---|---|---|
| BOOT | `0x0200_0000` | 128 KB |
| CPU0_FW | `0x0202_0000` | 640 KB |
| CPU1_FW | `0x020C_0000` | 256 KB |

양 끝을 고정하는 정렬 조건이 둘 있다. CPU0 의 초기 벡터 `0x0200_0000` 은 하드웨어로
고정이라 부트로더가 맨 앞이어야 한다. 그리고 `CPU1INITVTOR` 은 하위 7비트를 버리므로
CPU1 의 벡터 테이블은 128 바이트 정렬이어야 한다 — CPU1 이 CPU0 이미지가 끝나는
자리가 아니라 떨어지는 `0x020C_0000` 에 있는 이유다. MRAM 자체가 강제하는 파티션
정렬은 없고, 실질적인 하한은 32 바이트 프로그래밍 단위다.

SRAM 은 일부러 고르지 않게 나눈다.

![1872 KB 의 SRAM 을 나누는 방법과 코어별 TCM](sram-partition.svg)

FSP 기본값은 반씩 나누는 것이지만, CPU0 가 디스플레이와 네트워크 스택과 파일시스템을
지고 있어서 더 많이 가져간다. 코어 간 버퍼는 MPU 로 캐시 불가로 표시한 별도 영역에
둔다 — Cortex-M85 에는 D-cache 가 있고, 캐시 가능한 메모리에 놓인 공유 버퍼는 clean
이나 invalidate 를 한 번 빠뜨리는 순간 아무 소리 없이 IPC 를 깬다.

그 위에 코어마다 자기 TCM 이 있고, 둘 다 자기 것을 같은 주소로 본다. CPU0 는 ITCM 과
DTCM 을 128 KB 씩, CPU1 은 CTCM 과 STCM 을 64 KB 씩 갖는다.

프레임버퍼, 카메라, 오디오 같은 큰 버퍼는 SRAM 에 넣지 않는다. `0x6800_0000` 의
32 MB SDRAM 으로 간다.

## 옵션 설정은 한 이미지만 갖는다

`option_setting_*` 섹션 — OFS0 부터 OFS3, BPS, SAS 와 OTP 항목들 — 은 부팅할 때 딱
한 번 의미가 있다. 두 이미지가 둘 다 내보내면 두 이미지가 같은 주소에 쓴다.

그래서 부트로더가 가지고, 애플리케이션은 링크에서 뺀다. 지금은 부트로더가 없고 CPU0
펌웨어가 거기에 아무것도 안 내보내서, 빌드 출력의 해당 섹션이 전부 `0 B` 로 나온다.
빠뜨린 게 아니라 맞는 결과다.

## 지금 어디까지

위의 숫자들은 헤더 하나에 모여 있고, 코어별 링커 스크립트는 생성된 기본값이 아니라
그 헤더에서 좁혀 온다 — CPU0 쪽은 이제 장치 전체가 아니라
`FLASH_LENGTH = 0x000c0000`, `RAM_LENGTH = 0x00160000` 이라고 적혀 있다.

부트로더 파티션 크기는 아직 초안이다. 이미지에 실제 크기가 생기면 확정하고, ITCM
재배치는 여기에 기대기 전에 하드웨어에서 측정한다.

## 링크

- [titan-mini](https://github.com/chcbaram/titan-mini)
- [두 번째 코어를 깨우는 건 쉽다. 깨어났는지 아는 게 어렵다](../waking-the-second-core/)
- [펌웨어 개발 노트](https://github.com/chcbaram/titan-mini/tree/e0b0dcf1cc8f503b62323c9668f18656d4df1211/firmware/docs)

<!--
sources (commit e0b0dcf1cc8f503b62323c9668f18656d4df1211):
- 영어판 index.md 의 한국어판. 사실 관계는 같은 출처에서 온다.
- firmware/docs/02-memory-map.md — 전체, 특히 2절(SRAM 크기), 3절(MRAM 특성), 4~5절(파티션), 7절(옵션 설정)
- firmware/ra8p1-fw/src/lib/ra_sdk/cm85/fsp_gen.ld, memory_regions.ld
- mram-layout.svg, sram-partition.svg — 영어판과 같은 그림을 쓴다. 라벨은 영어다.
-->
