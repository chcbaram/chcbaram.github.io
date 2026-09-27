---
title: "SRAM 크기가 세 군데서 다르게 나온다"
date: 2026-09-27T03:58:04+09:00
description: "RA8P1 의 SRAM 이 얼마인지를 디바이스 팩과 데이터시트와 링커 스크립트가 서로 다르게 말한다. 어느 쪽이 맞는지 가린 이야기와, 부트로더가 어디서 돌아야 하는지를 결정해 버린 MRAM 제약."
projects: ["titan-mini"]
tags: ["ra8p1", "renesas", "memory", "linker", "mram", "firmware"]
series: ["Titan Mini (RA8P1)"]
repo: "https://github.com/chcbaram/titan-mini"
image: "mram-layout.svg"
ai_assisted: true
naver_url: ""
draft: false
---

Titan Mini 보드에서 메모리를 두 코어로 나누려면 먼저 답할 것이 둘 있었다.
`R7KA8P1KFLCAC` 의 SRAM 은 실제로 얼마인가. 그리고 MRAM 에서 코드를 돌리면서 그 MRAM 에
쓸 수 있는가.

둘 다 답이 예상한 곳에 없었다.

## 세 군데가 서로 다른 말을 한다

| 출처 | 값 |
|---|---|
| DFP 디바이스 팩 (칩 정보를 담은 벤더 배포 패키지) | `0x1A_0000` — 1664 KB |
| 데이터시트 | "1664 KB user SRAM" |
| FSP 가 생성한 링커 스크립트 | `0x1D_4000` — **1872 KB** |

208 KB 차이다. 반올림으로 생길 수 있는 양이 아니다. 혼자 다른 말을 하는 쪽이 링커
스크립트인데, 맞는 쪽도 링커 스크립트다.

하드웨어 매뉴얼의 메모리 맵을 보면 정리된다.

```
0x2200_0000 ~ 0x2219_FFFF   S0BI/S1BI/S2BI/S3BI   1664 KB
0x221A_0000 ~ 0x221D_3FFF   S0BI/S1BI/S2BI/S3BI    208 KB
```

두 항목이 주소상 이어져 있고 사이에 구멍이 없다. 합치면 `0x1D_4000`, 1872 KB 다.
디바이스 팩과 데이터시트가 첫 블록까지만 세고 만 것이다.

그래서 링커에는 `0x1D_4000` 을 준다. 데이터시트를 믿었으면 208 KB 를 통째로 놓칠
뻔했다. CPU1 에 배정한 전체보다 많은 양인데, 링커가 모르면 아무도 못 쓴다.

## MRAM 은 뱅크가 하나다. 그게 많은 걸 정해 버린다

RA8P1 은 코드를 플래시가 아니라 MRAM(자기저항 방식의 비휘발성 메모리) 에 넣는다.
성질은 대체로 쓰기 편하다. FSP 가 모는 기준으로 쓰기 단위가 32 바이트고, ECC 가 2비트
오류를 고치고 3비트 오류를 잡아내며, 따로 지우는 단계가 없다.

불편한 성질이 하나 있다. 매뉴얼의 병렬 접근 항목에 이렇게 적혀 있다.

- 백그라운드 동작(쓰는 중에 다른 곳을 읽는 것) 은 **서로 다른 MRAM 뱅크 사이에서만** 된다.
- 같은 매크로에 대한 읽기와 쓰기는 중재되고, 절대 동시에 돌지 않는다.
- 쓰는 중에는 인터럽트나 예외가 코드 MRAM 에서 벡터를 못 가져온다.

RA8P1 의 뱅크는 하나다. 그러니 백그라운드 동작은 아예 못 쓴다. MRAM 에서 실행하면서
MRAM 에 쓰는 것은 권장하지 않는 정도가 아니라 성립하지 않는다. 쓰기가 끝날 때까지
명령어를 못 가져오는데, 그 쓰기가 끝나기를 기다리는 폴링 루프 자신이 바로 그 명령어를
못 가져오기 때문이다.

**MRAM 에 쓰는 코드는 RAM 에서 돌아야 한다.** 부트로더 설계에서 이건 나중에 붙일
세부가 아니다. 구조를 여기서부터 정해야 한다. 본체는 통째로 ITCM(코어에 직접 붙은
명령어 전용 고속 RAM) 으로 옮기고, MRAM 에는 벡터와 스타트업 코드와 복사 테이블만
남긴다.

![MRAM 파티션 계획. 부트로더 본체는 ITCM 으로 재배치된다](mram-layout.svg)

## 링커가 이미 할 줄 안다

자기를 복사하는 부트 스텁을 직접 짜야 할 줄 알았다. 그런데 FSP 가 생성한 링커
스크립트에 "MRAM 에서 로드해서 RAM 에서 실행하는" 섹션이 이미 정의돼 있었다.

`src/lib/ra_sdk/cm85/fsp_gen.ld`

```
__itcm_from_flash$$ : { *(.itcm_from_flash) *(.itcm_code_from_flash) } > ITCM AT > FLASH
__dtcm_from_flash$$ : { *(.dtcm_from_flash) *(.dtcm_code_from_flash) } > DTCM AT > FLASH
__ram_from_flash$$  : { *(.ram_from_flash)  *(.ram_code_from_flash)  } > RAM  AT > FLASH
```

[커밋 e0b0dcf 의 소스](https://github.com/chcbaram/titan-mini/blob/e0b0dcf1cc8f503b62323c9668f18656d4df1211/firmware/ra8p1-fw/src/lib/ra_sdk/cm85/fsp_gen.ld)

`$$Base` / `$$Limit` / `$$Load` 심볼이 BSP 의 복사 테이블에 들어가고,
`SystemRuntimeInit()` 이 `SystemInit()` 안에서, `main()` 보다 먼저 복사를 끝낸다.
`.data` 를 초기화하는 것과 같은 장치다.

결국 소스에 속성 하나 붙이는 걸로 끝났다.

```c
#define BOOT_CODE   __attribute__((section(".itcm_code_from_flash")))
```

나머지 MRAM 규칙은 흔한 것들이다. 쓰는 중에 주파수를 바꾸거나 스탠바이로 가지 말 것,
쓰고 나면 배리어와 플러시와 완료 대기를 둘 것. 그 대기에서 CPU 를 세우지 않으려면 더미
읽기 대신 `MRCPS.PRGBSYC` 를 폴링한다.

## 파티션 계획

부트로더가 생기면 MRAM 은 세 영역이 된다. 지금은 CPU0 펌웨어가 다 쓰고 있다.

| 영역 | 시작 | 크기 |
|---|---|---|
| BOOT | `0x0200_0000` | 128 KB |
| CPU0_FW | `0x0202_0000` | 640 KB |
| CPU1_FW | `0x020C_0000` | 256 KB |

양 끝은 정렬 조건 둘이 붙잡고 있다. CPU0 의 초기 벡터 주소 `0x0200_0000` 은 하드웨어로
고정이라 부트로더가 맨 앞이어야 한다. 그리고 `CPU1INITVTOR`(CPU1 의 벡터 주소를 넣는
레지스터) 이 하위 7비트를 버리므로 CPU1 의 벡터 테이블은 128 바이트 정렬이어야 한다.
CPU1 이 CPU0 이미지가 끝나는 자리가 아니라 딱 떨어지는 `0x020C_0000` 에 있는 이유다.
MRAM 자체는 파티션 정렬을 요구하지 않고, 실질적인 하한은 32 바이트 쓰기 단위다.

SRAM 은 일부러 고르지 않게 나눈다.

![1872 KB 의 SRAM 을 나누는 방법과 코어별 TCM](sram-partition.svg)

FSP 기본값은 반씩 나누는 것이다. 그런데 CPU0 가 디스플레이와 네트워크 스택과
파일시스템을 지고 있어서 더 많이 가져간다. 코어 사이에 주고받는 버퍼는 MPU(메모리 보호
유닛) 로 캐시 불가로 표시한 별도 영역에 둔다. Cortex-M85 에는 D-cache 가 있는데, 캐시
가능한 메모리에 공유 버퍼를 두면 clean 이나 invalidate 를 한 번 빠뜨리는 순간 아무 소리
없이 통신이 깨진다.

그 위에 코어마다 자기 TCM 이 있고, 둘 다 자기 것을 같은 주소로 본다. CPU0 는 ITCM 과
DTCM 을 128 KB 씩, CPU1 은 CTCM 과 STCM 을 64 KB 씩 갖는다.

프레임버퍼, 카메라, 오디오 같은 큰 버퍼는 SRAM 에 안 넣는다. `0x6800_0000` 의 32 MB
SDRAM 으로 보낸다.

## 옵션 설정은 한 이미지만 갖는다

`option_setting_*` 섹션 — OFS0 부터 OFS3, BPS, SAS 와 OTP 항목들 — 은 부팅할 때 딱 한 번
쓰인다. 두 이미지가 둘 다 내보내면 같은 주소에 두 번 쓰게 된다.

그래서 부트로더가 갖고, 애플리케이션은 링크에서 뺀다. 지금은 부트로더가 없고 CPU0
펌웨어가 거기에 아무것도 안 내보내서 빌드 출력의 해당 섹션이 전부 `0 B` 로 찍힌다.
빠뜨린 게 아니라 맞는 결과다.

## 지금 어디까지

위의 숫자는 헤더 하나에 모아 뒀다. 코어별 링커 스크립트도 생성된 기본값이 아니라 그
헤더에서 좁혀 온다. CPU0 쪽은 이제 장치 전체가 아니라 `FLASH_LENGTH = 0x000c0000`,
`RAM_LENGTH = 0x00160000` 이라고 적혀 있다.

부트로더 파티션 크기는 아직 초안이다. 이미지에 실제 크기가 생기면 확정한다. ITCM
재배치도 여기에 기대기 전에 하드웨어에서 재 볼 생각이다.

## 링크

- [titan-mini](https://github.com/chcbaram/titan-mini)
- [두 번째 코어를 깨우는 건 쉽다. 깨어났는지 아는 게 어렵다](../waking-the-second-core/)
- [펌웨어 개발 노트](https://github.com/chcbaram/titan-mini/tree/e0b0dcf1cc8f503b62323c9668f18656d4df1211/firmware/docs)

<!--
sources (commit e0b0dcf1cc8f503b62323c9668f18656d4df1211):
- 영어판 index.md 와 같은 출처. 번역이 아니라 한국어로 다시 썼다.
- 용어 방침: 바로 안 읽히는 말은 첫 등장에 괄호로 뜻을 붙인다 (DFP 디바이스 팩, MRAM,
  백그라운드 동작, ITCM, MPU, CPU1INITVTOR). 저장소 한국어 문서의 낱말이라고 무조건
  따르지 않는다 — 그 문서도 Claude 가 쓴 것이라 낱말 자체에 권위가 없다.
- 제목은 firmware/docs/02-memory-map.md §2 "SRAM 크기 — 세 군데가 서로 다르다" 를 따랐다.
- firmware/docs/02-memory-map.md — 전체, 특히 2절(SRAM 크기), 3절(MRAM 특성), 4~5절(파티션), 7절(옵션 설정)
- firmware/ra8p1-fw/src/lib/ra_sdk/cm85/fsp_gen.ld, memory_regions.ld
- mram-layout.svg, sram-partition.svg — 영어판과 같은 그림을 쓴다. 라벨은 영어다.
-->
