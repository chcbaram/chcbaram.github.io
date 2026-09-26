---
title: "Waking the Second Core Is Easy. Knowing It Woke Is Not."
date: 2026-09-27T03:39:00+09:00
description: "Renesas FSP gives you exactly one function to start the second core on an RA8P1 — no return value, no way to ask whether it is alive. Here is the handshake I had to build, and the two traps that cost me the most time."
projects: ["titan-mini"]
tags: ["ra8p1", "renesas", "cortex-m33", "dual-core", "firmware", "debugging"]
series: ["Titan Mini (RA8P1)"]
repo: "https://github.com/chcbaram/titan-mini"
image: "dualcore-start.svg"
ai_assisted: true
naver_url: ""
draft: true
---

The RA8P1 on the Titan Mini board has two cores: a Cortex-M85 at 1 GHz as CPU0
and a Cortex-M33 as CPU1. Starting CPU1 turned out to be one function call.
Finding out whether it actually started took considerably longer, and two of the
problems along the way were not in my code at all.

## Where CPU1 lives

MRAM and SRAM are split per core, with the numbers kept in one header so the
linker scripts and the startup code cannot disagree.

| Region | Start | Size |
|---|---|---|
| MRAM CPU0 | `0x0200_0000` | 768 KB |
| MRAM CPU1 | `0x020C_0000` | 256 KB |
| SRAM CPU0 | `0x2200_0000` | 1408 KB |
| SRAM CPU1 | `0x2216_0000` | 384 KB |
| SRAM shared | `0x221C_0000` | 80 KB |

CPU1 starts at `0x020C_0000` rather than somewhere more convenient because
`CPU1INITVTOR` discards the low seven bits — the vector table has to be 128-byte
aligned. Putting CPU1 at the *top* also means the bootloader can later take
128 KB off the front of CPU0's region without moving CPU1.

## One function, no answer

FSP's entire multicore API is `R_BSP_SecondaryCoreStart()`. It writes three
registers — the vector address, a wait-release, and a keyed start request — and
returns `void`.

There is no call anywhere in FSP that asks whether the second core started, or
whether it is still running. There is an IPC semaphore and an NMI request, but
those are mutual exclusion and notification, not status.

So the answer has to be built. Everything below exists because that one function
tells you nothing.

![CPU1 start sequence: CPU0 sets the vector address, releases the wait and requests the start; CPU1 begins executing and writes a magic word into shared memory, which CPU0 waits for](dualcore-start.svg)

Steps ② ③ ④ are the three registers that one function writes. Steps ⑥ and ⑦ —
the part that actually tells you whether it worked — are mine, and the rest of
this post is about why they look the way they do.

## The macro that decides whether any of this compiles

FSP decides a project is multicore by checking whether one macro is defined:

```c
/* fsp/src/bsp/mcu/all/bsp_common.h */
#if defined(BSP_PARTITION_FLASH_CPU1_S_START)
 #define BSP_MULTICORE_PROJECT    (1)
#else
 #define BSP_MULTICORE_PROJECT    (0)
#endif
```

`R_BSP_SecondaryCoreStart()` sits inside that condition, so without the macro the
function does not exist at all. Renesas' configurator emits those partition
macros only for a "Solution" project — and the standalone configurator cannot
generate a Solution headlessly, which is the generation path this repository
uses.

So I define them myself, in one header that both cores' generated
`bsp_linker_info.h` includes at the spot reserved for it. The naming follows the
configurator's own template, `BSP_PARTITION_<RESOURCE>_<CPU0|CPU1>_<S|NS>_START`,
so a future Solution-generated build lines up.

## It wakes even when there is nothing to wake

That macro is now always defined, which means `BSP_MULTICORE_PROJECT` is always
true — including when I build without the CPU1 image. CPU0 was dutifully starting
CPU1 at `0x020C_0000`, where there was nothing. CPU1 read an erased vector table
and faulted. CPU0 never waits for a result, so everything looked fine.

The fix ties the build configuration to the runtime decision:

```cmake
-D_HW_DEF_CPU1_IMAGE=$<BOOL:${BUILD_CM33}>
```

and the header defaults it to `0` when undefined — **not waking is the safe
default.** Checking the vector table at runtime would be more general, but it
cannot tell a valid image from a stale one left over from a previous flash. That
moves to a real image header with a CRC when the bootloader arrives.

## Knowing it is alive

CPU1 reports itself through a struct in the shared SRAM region, placed at the
same address by both linker scripts.

`src/cpu/shared/shared.h`

```c
#define SHARED_MAGIC   0x544D5348UL   /* "TMSH" */
#define SHARED_VERSION 2

typedef struct
{
  volatile uint32_t magic;
  volatile uint32_t version;
  volatile uint32_t peer_alive;
  volatile uint32_t peer_tick;

  /* the peer introduces itself; written before magic, never changed after */
  volatile uint32_t peer_clock;              // Hz
  char              peer_name[SHARED_NAME_MAX];
  char              peer_fw_ver[SHARED_VER_MAX];
} shared_t;
```

[Source at commit e0b0dcf](https://github.com/chcbaram/titan-mini/blob/e0b0dcf1cc8f503b62323c9668f18656d4df1211/firmware/ra8p1-fw/src/cpu/shared/shared.h)

The section is `NOLOAD`: not carried in either image, not zeroed at startup. It
has to be, because whichever core boots second would otherwise wipe what the
first one wrote. Each core initialises only its own fields, and writes `magic`
**last**, behind a `__DMB()`. The first time I got that order wrong, CPU0 read a
counter that started at 1.3 billion.

### The trap: a stale magic looks alive

`NOLOAD` means nobody clears it — and SRAM survives a CPU0 reset. So the magic
word from a previous session stays valid-looking even when CPU1 is gone. I
measured this after erasing the entire CPU1 partition to `0xFFFFFFFF`:

```
magic   : 0x544D5348      ← looks valid
alive   : 65303  (+0 / 500ms)
tick    : 8231700 ms  (+0)
```

The only thing telling the truth was `+0`. The counters were not moving.

The fix is on the CPU0 side: **clear `magic` immediately before requesting the
start**, then wait for it to appear. Only then does its presence mean anything.

```
CPU0   clear magic → request start → wait up to 100 ms for magic
CPU1   initialise own fields → __DMB() → write magic last
```

Measured handshake time: **1 ms**.

### The primary core cannot compute the peer's clock

`peer_clock` is in that struct because the two cores do not run at the same
speed. They are divided separately — `SCKDIVCR2.CPUCK0` and `CPUCK1` — and CPU1
skips clock initialisation entirely. Measured: **CPU0 at 1000 MHz, CPU1 at
250 MHz**. CPU0 has no way to derive that, so CPU1 reports it.

## The probe stopped working

Once CPU1 was genuinely running, flashing started failing:

```
AHB-AP#2 ... [0]<e000e000:SCS M33 class=9 designer=43b:Arm part=d21 ...>
CPU core #0: Cortex-M85 r1p1, v8.1-M architecture
Error: <APv1Address@0x106734610 #2 dp=0>
```

This was not my firmware. The device pack declares both processors but never
says which access port each one is on — there is only a single `<debug>` element
with an SVD path. pyOCD reads `Pname` plus an AP id from those elements; with
neither present it maps the first processor to AP#0 and nothing else. The moment
a Cortex-M33 appears on AP#2, the lookup raises `KeyError`.

While CPU1 was asleep, AP#2 never answered and the problem stayed hidden.

The fix is two lines in the pack, with the AP numbers taken from an actual scan:

```xml
<subFamily DsubFamily="RA8P1_1M_DualCore">
  <debug Pname="CPU0" __ap="0"/>
  <debug Pname="CPU1" __ap="2"/>
```

If you are bringing up an RA8P1 and your probe dies the day the second core
starts working, this is worth checking before you suspect your own code.

## One more thing: CPU1 does not own pins

CPU1's configuration has no pin settings at all. Every pin — including pins for
peripherals CPU1 uses — is configured by CPU0. FSP's secondary build only ANDs
into the pin security attribute register rather than assigning it, so it can
narrow what CPU0 granted but never widen it. Splitting pin ownership between two
configurators would mean two files that have to agree, with nothing enforcing it.

## Where it stands

CPU1 boots, reports its name, firmware version and clock, and CPU0 can ask at any
time whether it is still running without blocking. The public interface is
functions only, named for a generic peer rather than `cpu1`, so the same header
works on a dual-core STM32 or an RP2040.

IPC messaging, cache coherency and an RTOS on CPU1 come next. Right now CPU1's
job is to prove it is there.

## Links

- [titan-mini](https://github.com/chcbaram/titan-mini)
- [Laying Out a Dual-Core Firmware Project, and Proving It With One LED](../titan-mini-firmware-skeleton/)
- [Firmware development notes](https://github.com/chcbaram/titan-mini/tree/e0b0dcf1cc8f503b62323c9668f18656d4df1211/firmware/docs) (Korean)

<!--
sources (commit e0b0dcf1cc8f503b62323c9668f18656d4df1211):
- firmware/docs/23-cm33-boot.md — 파티션, 매크로, 기동, 공유 블록, pyOCD/DFP, 핀
- firmware/docs/04-dualcore.md, 02-memory-map.md — 코어 구성과 주소 공간
- firmware/ra8p1-fw/src/cpu/shared/shared.h, src/common/hw/include/ipc.h, src/cpu/cm85/hw/driver/ipc.c
- dualcore-start.svg — 저장소 firmware/docs/images/dualcore-start.svg 를 옮겨 그린 것.
  라벨을 영어로 바꾸고, ⑥⑦ 단계를 실제 코드(ipc.c)에 맞춰 공유 블록 magic 핸드셰이크로
  고쳤다. 원본은 R_BSP_IpcSemaphoreTake/Give 로 그려져 있는데 코드는 그것을 쓰지 않는다.
-->
