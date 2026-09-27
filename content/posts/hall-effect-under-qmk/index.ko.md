---
title: "QMK 를 포크하지 않고 그 아래에 홀이펙트를 끼웠다"
date: 2026-09-27T11:00:00+09:00
description: "홀이펙트 키보드 펌웨어는 보통 키 판정을 새로 쓰고, 그러다 보면 그 위도 전부 새로 쓰게 된다. 나는 QMK 를 그대로 두고 밑에서 판정만 갈아 끼웠다. 그래서 레이어와 매크로와 탭홀드가 그대로 돌고, VIA 는 QMK 자신의 via.c 로 붙는다."
projects: ["wish-he"]
tags: ["hall-effect", "keyboard", "qmk", "via", "firmware", "hpm5361", "architecture"]
series: ["WISH HE"]
repo: "https://github.com/chcbaram/wish-he"
image: "qmk-he-stack.svg"
ai_assisted: true
naver_url: ""
draft: false
---

`wish-he` 는 시판 홀이펙트 키보드에 올리는 커스텀 펌웨어다. HPM5361(RISC-V,
400 MHz) 에서 돌고, 내가 설계하지 않은 보드의 앱 자리만 바꿔 쓴다. 보드에 원래 있던
IAP 부트로더는 그대로 두니 언제든 순정으로 돌아간다.

재미있는 건 홀이펙트 계산이 아니다. **어디서 잘랐나** 다. 홀이펙트 펌웨어는 보통 키
판정을 새로 쓰는데, 한 번 그러고 나면 레이어도 매크로도 탭홀드도 설정 도구도 결국 다
새로 쓰게 된다. 그 값을 치르기 싫었다. 그래서 QMK 는 그대로 두고 그 밑에 있는 것 하나,
**키가 눌렸는지 정하는 부분만** 갈아 끼웠다.

![WISH60 HE(Geonworks VENOM 60HE-7U) 에 펌웨어를 올리는 중. 키별 LED 가 켜진 맨 PCB, 디버그 프로브로 가는 리본, 전원과 콘솔용 USB-C](01.jpg)

## 왜 남의 보드인가

원래는 보드를 직접 만들 생각이었다. 두 가지가 그걸 뒤로 미뤘다.

PCB 를 뜨는 값이 싸지 않다. 그리고 펌웨어가 도는지도 모르는 채로 그 돈을 먼저 쓰게
된다. 두 번째 이유가 더 크다. 자기가 설계한 보드에 새 펌웨어를 올리면 버그 하나가
나올 때마다 후보가 둘이다 — 하드웨어인가 코드인가. 이미 도는 하드웨어에서 시작하면 그
질문이 아예 없다. 나중에 내 보드를 만들 때 펌웨어는 이미 검증된 물건이고, 깨지는 게
있으면 보드다.

시판 홀이펙트 키보드는 처음 홀이펙트를 구현해 보는 데 좋은 레퍼런스이기도 하다.
스위치도 센서 배치도 아날로그 경로도, 누군가 이미 정하고 물건으로 내놓은 것들이다.

## 어디서 잘랐나

접점 키보드는 펌웨어에 눌렸다/안 눌렸다를 준다. 홀이펙트 스위치는 자석이 얼마나
움직였는지를 카운트로, 스캔할 때마다 준다. 그 추가 정보가 핵심이다 — 래피드 트리거가
그걸 먹고 산다. 그런데 **판정 계층 위로는 아무도 그걸 안 궁금해한다.** 일단 눌린
것으로 정해지고 나면, 키맵 찾기는 그냥 키맵 찾기다.

그래서 `keys.c` 가 스캔하고 거르고 눌림을 정한 다음, QMK 에 행 비트마스크를 건넨다.
QMK 는 자기가 어떤 스위치를 상대하는지 끝내 모른다.

![홀이펙트 판정이 QMK 의 매트릭스 자리를 채운다. keys.c 가 스캔·필터·판정을 하고 port/matrix.c 로 행 비트마스크를 올리면, 그 위는 손대지 않은 QMK 다](qmk-he-stack.svg)

비트마스크는 애초에 `matrix_row_t` 와 비트 단위로 맞춰 만들었다. 프로젝트에 QMK 가
아예 없던 시절에 그렇게 해 뒀다. 그래서 연결부가 하는 일이 복사뿐이다.

`firmware/wish-he/src/hw/driver/keys.c`
([퍼머링크](https://github.com/chcbaram/wish-he/blob/2d5083019c522b35f0fe0d7c4f6d8df51b99d22f/firmware/wish-he/src/hw/driver/keys.c#L5028-L5036))

```c
/*
 * 행 비트마스크를 그대로 준다. QMK 의 matrix_row_t 와 비트 순서가 같아서
 * 상위 계층은 이 보드가 HE 인지 일반 매트릭스인지 몰라도 된다.
 */
uint16_t keysGetRow(uint16_t row)
{
  if (row >= KEYS_STEP_MAX) return 0;
  return pressed[row];
}
```

`firmware/wish-he/src/ap/modules/qmk/port/matrix.c`
([퍼머링크](https://github.com/chcbaram/wish-he/blob/2d5083019c522b35f0fe0d7c4f6d8df51b99d22f/firmware/wish-he/src/ap/modules/qmk/port/matrix.c#L75-L83))

```c
  bool live = keysIsReportEnabled();

  for (uint8_t r = 0; r < MATRIX_ROWS; r++)
  {
    curr[r]  = live ? keysGetRow(r) : 0;   /* 비트 순서가 같아 그대로 받는다 */
    changed |= (matrix_row_t)(curr[r] ^ matrix[r]);
  }

  if (changed) memcpy(matrix, curr, sizeof(matrix));
```

측정 명령이 도는 동안에는 `live` 가 거짓이다. QMK 에 0 을 먹이면 QMK 가 알아서 "전부
떼졌다" 고 판단하고 빈 리포트를 낸다. 그래서 내가 안 보는 사이에 눌린 채로 남는 키가
없다.

## QMK 에 안 넘기는 것

**디바운스.** QMK 의 매트릭스 계층은 금속 접점을 전제해서, 떨림을 넘기려고 변화를 몇
밀리초 붙들고 있는다. 기본값이 5 ms 다. 홀이펙트 스위치에는 접점이 없으니 튈 것도
없다. 디바운스는 거를 게 없으면서 지연만 더한다. 그래서 `port/matrix.c` 는 그걸 아예
안 부른다. 잡음은 더 아래에서 데드밴드 필터와, 누를 때와 뗄 때를 따로 둔 문턱으로
잡는다. 둘 다 지연이 0 이다. 누름은 행정의 30 %, 뗌은 19 % 이고 그 사이가
히스테리시스다.

30/19 로 갈라 둔 게 보기보다 중요하다. 예전 필터는 1차 IIR 이었는데, 그 정착 시간이
그대로 입력 지연에 얹혔다. 63 % 까지 152 us, 90 % 까지 342 us. 데드밴드 판은 같은
표본 안에서 반응한다.

**래피드 트리거.** 0.1 mm 단위의 방향 반전을 본다. 이걸 QMK 루프에서 돌리면 자기 주기보다
훨씬 잔 움직임을 표본으로 잡는 셈이다. 그래서 `keys.c` 안에서, 스캔 속도로 돈다.

**나머지는 전부 QMK 로 간다.** 그리고 거기서 QMK 는 싸다. `action_exec` 는 키가 바뀔
때만 돌기 때문이다. 빨리 치는 사람이 초당 수백 번을 만드는데, 8 kHz 폴링과는 아무
상관이 없는 숫자다.

## 루프는 둘, 슈퍼루프는 하나

`firmware/wish-he/src/ap/ap.c`
([퍼머링크](https://github.com/chcbaram/wish-he/blob/2d5083019c522b35f0fe0d7c4f6d8df51b99d22f/firmware/wish-he/src/ap/ap.c#L46-L58))

```c
void update(void const *arg)
{
#if defined(_USE_HW_LED)
  updateLED();
#endif

  keysUpdate();                       /* ADC 스캔 + 눌림 판정 */
  if (qmkIsOn()) qmkUpdate();         /* 키맵 · 레이어 · 매크로 · VIA -> HID 리포트 */

  usbUpdate();                        /* HID 로 들어온 부트/리셋/트래킹 요청 처리 */
  keysCfgUpdate();                    /* 바뀐 설정을 조용해진 뒤 한 번 저장 */
  keysSwUpdate();                     /* 바뀐 스위치 정의도 (플래시라 ISR 밖) */
}
```

이게 설계의 정직한 판이다. 둘은 개념상 독립이지만 여전히 슈퍼루프 하나라서, QMK 가
느려지면 스캔도 느려진다. QMK 를 처음 링크했을 때 스캔이 38 us 에서 62 us 로 늘어난
것도 정확히 그 이유였다. 그때 나는 래피드 트리거를 제대로 하려면 스캔을 ADC 완료
인터럽트로 빼야겠다고 적어 뒀다.

그리고 제대로 재 보니 원인이 구조가 아니었다. `-O0` 과 명령어 캐시 축출이었다. `-O2`
로 바꾸고 스캔 경로를 ILM 에 올리니 한 바퀴 26 us, 초당 38,000 바퀴가 됐고, 분리해야
할 이유가 급하지 않게 됐다.

여전히 보장이 아니라 예산이다. 만들지도 않은 분리를 만들었다고 하는 대신 이렇게 적어
둔다.

![보드에서 `qmk info` 를 친 결과](qmk-info-w560.png)

![`matrix info`. 디바운스가 "없음" 인 이유는 홀이펙트 스위치에 튈 접점이 없기 때문이다](matrix-info-w400.png)

## VIA 흉내가 아니라 VIA 그 자체

설정 도구가 보통 이런 프로젝트의 성패를 가른다. VIA 호환 프로토콜을 짠다는 건 `via.c`
가 하는 일을 그대로 재현한다는 뜻이다. 어차피 그럴 거면 `via.c` 를 컴파일하는 게 낫다.
그래서 `dynamic_keymap.c` 와 함께 빌드에 들어가 있고, 키맵은 16 KB 짜리 에뮬레이션
EEPROM 에 산다.

QMK 의 EEPROM API 는 바이트 단위로 아무 때나 쓸 수 있어야 하는데 NOR 플래시는 그게
안 된다. 그래서 쓰기는 RAM 그림자에 앉고 해당 섹터만 더럽다고 표시한다. 실제로 굽는
것은 200 ms 조용해진 뒤에, 한 번에 한 섹터씩이다. VIA 에서 키맵을 바꾸면 바이트 쓰기가
수백 번 연달아 들어오는데, 그때마다 구우면 같은 섹터를 수백 번 지우게 된다. 그동안
인터럽트가 막히고 USB 가 선다.

우리 홀이펙트 명령은 원래 `0x01`/`0x02`/`0x03` 이었다. `id_get_protocol_version` 같은
것들과 정면으로 부딪힌다. QMK 가 들어오기 전에, 아직 그 도구를 나 혼자 쓸 때
`0xC0`~`0xCB` 로 옮겼다. 일부러 남긴 예외가 하나 있다. 부트로더 점프는 VIA 자신의
`0x0B` 를 그대로 쓴다. 순정 VIA 도구로도 보드를 업데이트 모드로 넣을 수 있게.

![설정 도구는 VIA 자신의 키맵 편집기에 탭 하나를 더한 것이다. 키맵·레이어·매크로는 순정 VIA 고, HALL EFFECT 탭만 우리 것이다](via-hall-effect-tab.png)

## QMK 를 실제로 얼마나 건드렸나

"하나도 안 건드렸다" 보다는 많고, 그림이 주장하던 것보다는 적다. `quantum` 트리는
통째로 들여왔다 — `.c` 파일 128개. 하지만 CMake 에 적힌 것만 컴파일되고, 그게 로깅과
send-string 글로브를 빼면 19개쯤이다. 들여온 커밋 이후로 트리 자체는 파일 넷에서 80줄
추가, 5줄 삭제가 됐다.

- `eeconfig.c` — NKRO 를 `FORCE_NKRO` 가 아니라 eeconfig 기본값으로 켰다. 사용자가
  여전히 끌 수 있게
- `dynamic_keymap.c` — 프로파일별 키맵 오프셋. VIA 가 키맵을 키 단위로도, 버퍼로도
  읽고 쓰기 때문에 두 군데를 고쳐야 했다
- `via.c`
- `keyboard.c` — 서스펜드 처리. upstream 은 이 포트에 없는 프로토콜 계층에서 한다

다 들어간 건 아니다. 키 오버라이드와 콤보는 컴파일에 안 들어간다. 아직 필요하다는
사람이 없었고, 생기면 넣는다. 그러면 내 README 의 "빠진 것이 없다" 는 과한 말이 맞고,
고칠 것은 빌드가 아니라 README 다.

`quantum` 트리는 이 작업을 하던 시점의 upstream 최신이었다. 포트가 들고 있는 표식은
`port/version.h` 의 `QMK_BUILDDATE "2024-04-23-11:29:54"` 하나뿐이라, 커밋 해시 대신
그 날짜가 실질적인 기준점이다.

## 치른 값

QMK 가 처음 들어갔을 때 `keyboard_task` 평균이 8 us 였다. 재 보기 전에는 알 수 없다고
적어 두었던 숫자고, 200 us 를 넘으면 125 us 폴링이 무의미해진다는 메모를 같이
달아 뒀었다.

지금은 표본 3억 1천만 개에서 평균 2 us 다. 한 바퀴 최악은 436 us 였고, 125 us 를 넘은
것은 딱 한 번, **부팅 449 ms 때** 다. 그 뒤로 2.7시간 도는 동안 없었다. 깔끔하게 0
이라고 적는 대신 이렇게 적어 둔다. 꼬리는 있고, 다만 그게 기동 구간에 산다.

![`keys lat` 은 경로를 다섯 구간으로 쪼갠다. 판정에서 ACK 까지가 6,893회 평균 92 us 이고, 그중 8 kHz 폴링 대기(4번)가 제일 큰 덩어리다](keys-lat-w560.png)

## 링크

- [wish-he](https://github.com/chcbaram/wish-he)
- [입력지점 위의 유령 입력, 신고 하나에 원인 둘](../wish-he-rapid-trigger/) — QMK
  밑에 앉은 래피드 트리거 계층이 실제로 무슨 일을 하는지, 그리고 거기 있던 버그 둘
- [via-he](https://github.com/chcbaram/via-he) — 설정 도구 포크
- [펌웨어 개발 노트](https://github.com/chcbaram/wish-he/tree/2d5083019c522b35f0fe0d7c4f6d8df51b99d22f/firmware/wish-he/docs)

<!--
sources (commit 2d5083019c522b35f0fe0d7c4f6d8df51b99d22f):
- 영어판 index.md 와 같은 출처. 번역이 아니라 한국어로 다시 썼다.
- 코드 발췌의 주석은 저장소 원본 그대로 한국어다. 영어판은 그것을 번역해 실었다.
- firmware/wish-he/docs/10-qmk.md, 11-via.md, 06-key-decision.md, 07-keyboard.md,
  12-scan-speed.md, checklist.md, README.md
- firmware/wish-he/src/hw/driver/keys.c L5028-5036, src/ap/modules/qmk/port/matrix.c L75-83,
  src/ap/ap.c L46-58, src/ap/modules/qmk/CMakeLists.txt, port/version.h
- qmk-he-stack.svg — 저장소 docs/images/qmk-he-stack.svg 를 옮기고 라벨을 영어로 바꾼 것.
  코드와 달랐던 라벨 셋(QMK 코어 "손대지 않는다", 키 오버라이드, 콤보)을 실제 빌드에 맞게 고쳤다.
- 01.jpg, qmk-info-w560.png, matrix-info-w400.png, keys-lat-w560.png — 저자 제공
-->
