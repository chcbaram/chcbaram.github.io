---
title: "펌웨어 뼈대를 세우고, LED 하나로 확인하기"
date: 2026-09-27T03:33:11+09:00
description: "MCU 가 바뀌어도 애플리케이션이 살아남게 펌웨어를 어떻게 나누는지, 그 규칙을 컴파일러가 왜 지켜 주지 못하는지, 대신 지켜 주는 스크립트는 무엇인지. Renesas RA8P1 보드의 첫 마일스톤에 대고 확인했다."
projects: ["titan-mini"]
tags: ["ra8p1", "renesas", "cortex-m85", "dual-core", "firmware", "cmake"]
series: ["Titan Mini (RA8P1)"]
repo: "https://github.com/chcbaram/titan-mini"
image: "01.jpg"
ai_assisted: true
naver_url: ""
draft: false
---

Titan Mini 는 Renesas `R7KA8P1KFLCAC` 로 만든 보드다. CPU0 가 1 GHz Cortex-M85, CPU1 이
Cortex-M33, 거기에 Ethos-U55 NPU 가 붙는다. 289볼 BGA 에 MRAM 1 MB 와 SRAM 1872 KB 다.
그게 재미있어지려면 먼저 프로젝트에 모양이 있어야 한다. 내가 정착한 모양과, 그 모양을
붙들고 있는 규칙 하나에 대한 글이다.

![책상 위의 Titan Mini. USB-C 로 전원과 가상 시리얼 콘솔, 리본 케이블로 CMSIS-DAP 프로브, LED3 의 빨강이 켜져 있다](01.jpg)

개발 셋업은 이게 전부다. 전원과 콘솔이 USB-C 로 들어오고, 리본 케이블은 `pyocd` 가 모는
CMSIS-DAP 프로브로 간다. LED3 의 빨강 채널이 켜져 있다.

## 구조

```
src/
├── common/     두 코어가 같이 쓰고, 프로젝트가 바뀌어도 그대로 간다
│   ├── core/       qbuffer, util_core
│   └── hw/include/ 공개 드라이버 API — led.h uart.h cli.h
├── cpu/        코어별, 손으로 쓴다
│   ├── shared/     두 코어가 합의해야 하는 계약
│   ├── cm85/       CPU0 — main / ap / bsp / hw
│   └── cm33/       CPU1
└── lib/ra_sdk/ 벤더 — FSP 소스와 코어별 생성 결과
```

`src/` 바로 아래는 전부 **분류**다. 인스턴스가 아니다. `cm85` 가 `cpu/` 옆이 아니라 안에
있어서, 나중에 코어를 하나 더 붙여도 최상위가 안 바뀐다.

디렉터리 이름이 `core/` 가 아니라 `cpu/` 인 이유는 둘이다. 여기서는 `common/core/` 가
이미 다른 뜻이고, FSP(Renesas 의 드라이버·설정 생성 프레임워크) 자신이 이것들을 CPU 라고
부른다 — `_RA_CORE=CPU0`.

`cpu/shared/` 는 어느 코어의 것도 아닌 것들이 사는 자리다. 지금은 공유 메모리 블록
배치뿐이고, 나중에 코어 간 메시지 정의가 들어간다. 이걸 `common/` 에 두지 않았다.
`common/` 은 MCU 가 바뀌어도 살아남아야 하는데, 이건 이 보드의 이 두 코어 사이에서만
뜻이 있는 약속이기 때문이다.

## 규칙 하나

> MCU 가 바뀌면 `bsp` 와 `hw/driver` 는 다시 쓴다. `ap` 와 `common` 은 안 건드린다.

| 계층 | 벤더 HAL (FSP / CMSIS) | 역할 |
|---|---|---|
| `ap/` | **금지** | 애플리케이션. 공개된 `hw/` API 만 부른다 |
| `common/` | **금지** | 이식 가능한 코드. 다른 저장소와 그대로 공유한다 |
| `cpu/shared/` | **금지** | 두 코어 사이의 약속 |
| `hw/driver/` | 허용 | **MCU 의존성이 갇히는 자리** |
| `bsp/` | 허용 | MCU 초기화, 클럭, 시간 |

`ap` 가 `hw` 드라이버를 부르는 건 정상 경로다. 규칙이 막는 것은 `ap` 가
`R_IOPORT_PinWrite()` 를 직접 부르는 쪽이다.

## 컴파일러는 이 규칙을 안 지켜 준다

적어 둘 만한 건 이 부분이다. 인클루드가
`ap_def.h` → `hw.h` → `hw_def.h` → `bsp.h` → `hal_data.h` 로 이어져서 모든 FSP 심볼이
`ap` 까지 그대로 보인다. 규칙을 어겨도 빌드가 안 깨진다. 의지만 믿으면 언젠가 샌다.
아마 피곤한 저녁일 것이고, 수상해 보이는 diff 는 확실히 아닐 것이다.

그래서 검사기를 뒀다.

`firmware/ra8p1-fw/tools/check_layers.py`

```python
# FSP / CMSIS vendor symbols. Both header names and identifiers are matched.
VENDOR = re.compile(
    r'\b('
    r'R_[A-Z][A-Za-z0-9_]*'       # R_IOPORT_Open, R_PORT1
    r'|FSP_[A-Z_]+'               # FSP_SUCCESS
    r'|fsp_err_t|fsp_[a-z_]+_t'
    r'|BSP_[A-Z0-9_]+'            # BSP_IO_PORT_01_PIN_09
    r'|bsp_[a-z0-9_]+_t'
    r'|g_ioport|g_uart[0-9]+'     # ra_gen instances
    r')\b'
)
```

[커밋 e0b0dcf 의 소스](https://github.com/chcbaram/titan-mini/blob/e0b0dcf1cc8f503b62323c9668f18656d4df1211/firmware/ra8p1-fw/tools/check_layers.py#L26-L38)

금지된 계층을 훑으면서 저 심볼들과 `hal_data.h`, `r_*.h` 같은 벤더 헤더를 찾는다. 걸리면
1 로 끝난다. 문서에만 있는 규칙은 이미 어딘가에서 깨져 있는 규칙이다.

## LED 하나로 고리 닫기

첫 마일스톤 자체는 재미있는 게 아니다. LED 깜빡이기다. 그래도 이걸로 빌드 → 굽기 →
확인이 한 바퀴 돌고, 계층 규칙이 처음으로 견뎌야 하는 대상이 된다.

보드의 RGB LED 는 공통 애노드가 `+3V3` 에 물려 있다. 그래서 모든 채널이 **액티브
로우** 다. 빨강 P109, 초록 P108, 파랑 P110.

여기서 두 가지가 따라 나왔다.

핀 설정의 초기 상태를 `IOPORT_CFG_PORT_OUTPUT_HIGH` 로 둔 것은 여기서 HIGH 가 *꺼짐*
이기 때문이다. 거꾸로 하면 부팅 중에 LED 가 깜빡인다. 이 설정은 `main()` 보다 먼저,
`R_BSP_WarmStart(POST_C)` 안의 `R_IOPORT_Open()` 이 적용한다. 그래서 드라이버는 핀 방향을
건드리지 않는다.

그리고 드라이버는 테이블이다. `R_IOPORT_*` 를 직접 부르지 않고 FSP 인스턴스의 함수
포인터로 부른다.

`src/cpu/cm85/hw/driver/led.c`

```c
static const led_tbl_t led_tbl[LED_MAX_CH] =
{
  {BSP_IO_PORT_01_PIN_09, BSP_IO_LEVEL_LOW, BSP_IO_LEVEL_HIGH},   // LED3 RED
  {BSP_IO_PORT_01_PIN_08, BSP_IO_LEVEL_LOW, BSP_IO_LEVEL_HIGH},   // LED3 GREEN
  {BSP_IO_PORT_01_PIN_10, BSP_IO_LEVEL_LOW, BSP_IO_LEVEL_HIGH},   // LED3 BLUE
};

void ledOn(uint8_t ch)
{
  if (ch >= LED_MAX_CH) return;

  g_ioport.p_api->pinWrite(g_ioport.p_ctrl, led_tbl[ch].pin, led_tbl[ch].on_state);
}
```

[커밋 e0b0dcf 의 소스](https://github.com/chcbaram/titan-mini/blob/e0b0dcf1cc8f503b62323c9668f18656d4df1211/firmware/ra8p1-fw/src/cpu/cm85/hw/driver/led.c)

테이블에 `on_state` 와 `off_state` 를 같이 들고 있으면, 액티브 하이 보드에는 다른
드라이버가 아니라 다른 테이블만 있으면 된다.

## 지금 어디까지

CPU0 는 1000 MHz 로 돈다. FreeRTOS 11.1.0, SCI2 위의 CLI, `.module` 섹션을 통한 모듈
자동 등록까지 올라가 있다. CPU1 은 기동을 확인할 만큼만 올렸고, 코어 간 통신과 캐시와
그쪽 RTOS 는 다음이다.

메모리는 코어별로 나눠 뒀다. CPU0 가 MRAM 768 KB 와 SRAM 1408 KB, CPU1 이 256 KB 와
384 KB, 공유가 80 KB 다. 지금 CM85 이미지는 플래시 38,512 B, RAM 78,340 B 를 쓴다.

다음은 GPIO 와 타이머, 그다음이 NVS 를 얹은 MRAM 이다. 부트로더 설계가 기대고 있는 ITCM
재배치를 실제로 재 보는 자리이기도 하다.

## 링크

- [titan-mini](https://github.com/chcbaram/titan-mini)
- [펌웨어 개발 노트](https://github.com/chcbaram/titan-mini/tree/e0b0dcf1cc8f503b62323c9668f18656d4df1211/firmware/docs)

<!--
sources (commit e0b0dcf1cc8f503b62323c9668f18656d4df1211):
- 영어판 index.md 와 같은 출처. 번역이 아니라 한국어로 다시 썼다.
- 용어 방침: 바로 안 읽히는 말은 첫 등장에 괄호로 뜻을 붙인다 (FSP). 저장소 한국어
  문서의 낱말이라고 무조건 따르지 않는다.
- README.md, firmware/docs/README.md — 보드/MCU 사양, 현재 상태, 빌드 크기, 파티션
- firmware/docs/12-project-skeleton.md — 디렉터리, 계층 규칙, 검사기
- firmware/docs/20-led.md — LED 하드웨어, 핀 설정, 드라이버
- firmware/ra8p1-fw/tools/check_layers.py, src/cpu/cm85/hw/driver/led.c
- 01.jpg — 저자가 제공한 디버깅 셋업 사진
-->
