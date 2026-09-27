---
title: "Reading Magnet Depth With an ADC"
date: 2026-09-27T13:51:30+09:00
description: "A Hall-effect key has no contact to close — it reports a voltage. This is the layer under my keyboard firmware that turns 64 magnets into 64 numbers every scan: an eight-channel ADC sequence, a gray-coded analog MUX, two register names that lie, and a noise floor I could not get past."
projects: ["wish-he"]
tags: ["hall-effect", "keyboard", "adc", "dma", "firmware", "hpm5361", "risc-v", "noise"]
series: ["WISH HE"]
repo: "https://github.com/chcbaram/wish-he"
image: "01.jpg"
ai_assisted: true
naver_url: ""
draft: true
---

`wish-he` is custom firmware for commercial Hall-effect keyboards, running on an
HPM5361 (RISC-V, 400 MHz). There is no switch matrix to strobe: every key sits over
a Hall sensor whose output moves with the distance to the magnet in the switch, so
"is this key down" starts life as an analog voltage. This post is about the layer
that turns those voltages into numbers — how the channels are multiplexed, what the
ADC sequencer actually does when you configure it, and where the noise floor turned
out to be. Millimetres, the press decision, and handing the result to QMK's matrix
layer all sit above this, and they are separate posts.

## What the board gives me

Eight analog pads go into the two ADC blocks — four channels on ADC0, four on
ADC1 — and a 3-bit MUX address selects which group of eight sensors is connected.
Eight channels by eight steps is 64 cells; WISH60 HE (7U) uses 63 and WISH61 HE
uses 61.

Two things about the pin map cost me time before a single sample was right. The ADC
channel number is not the pad number: `PB00~PB07` map to `ch8~ch15` and `PB08~PB15`
map to `ch0~ch7`, rotated by eight, so the sequence tables are neither sorted nor
contiguous. And the `PY` pads carrying the MUX address need `PIOC` set to ALT3 as
well as `IOC`, or the pad is simply not wired to the SoC.

None of that came with documentation. The board is somebody else's product, so the
sensor rotation and the multiplexer wiring were worked out from the board itself
before any of this code existed.

![One scan: 64 sensors reach the ADC eight at a time, through a 3-bit multiplexer address stepped in gray-code order](scan-structure.svg)

![The WISH60 HE board with most switches out. Every cell has its own Hall sensor on the pad, and the analog multiplexers sit under the centre strip](01.jpg)

## The scan loop

`firmware/wish-he/src/hw/driver/keys.c`
([permalink](https://github.com/chcbaram/wish-he/blob/2d5083019c522b35f0fe0d7c4f6d8df51b99d22f/firmware/wish-he/src/hw/driver/keys.c#L51-L54))

```c
static const uint8_t mux_addr[KEYS_STEP_MAX + 1] =
{
  6, 7, 5, 4, 0, 1, 3, 2,   6
};
```

Two decisions sit in that one line. The order is a gray code, so only one address
bit changes per step and crosstalk between neighbouring channels is smaller. And a
ninth element repeats the first, because the loop writes the *next* address before
reading this step's results — the settling of step N+1 then overlaps the processing
of step N and costs nothing. Settling is 16 cycles, about 40 ns at 400 MHz. There
is no timer; the scan free-runs in the main loop.

## Two register names that lie

Getting the first conversion out of the sequencer took two rounds of "the
completion interrupt never arrives", both of them me trusting a field name.

`SEQ_INT_EN` sounded like "use the sequence completion interrupt", so I set it
`false` everywhere. It is per queue element: *tell me when this element finishes*.
With none of them set, `SEQ_CMPT` never rises at all — 174 scans, 174 timeouts.

`CONT_EN` sounded like "repeat continuously", so I turned it off. The manual says
it means *continue processing the queue till end(seq_len) after trigger once*. With
it off, one trigger converts exactly one channel and stops: the DMA buffer had one
real word and three untouched. Repeating is `RESTART_EN`, and only alongside
`CONT_EN`.

`firmware/wish-he/src/hw/driver/keys.c`
([permalink](https://github.com/chcbaram/wish-he/blob/2d5083019c522b35f0fe0d7c4f6d8df51b99d22f/firmware/wish-he/src/hw/driver/keys.c#L1584-L1596))

```c
seq_cfg.cont_en    = true;
seq_cfg.restart_en = false;
for (uint32_t i = 0; i < KEYS_SEQ_LEN; i++)
{
  seq_cfg.queue[i].ch = seq_ch[i];

  /* SEQ_INT_EN is per queue element, not per sequence.
     Enable only the last one: one interrupt at the end of the sequence. */
  seq_cfg.queue[i].seq_int_en = (i == (KEYS_SEQ_LEN - 1));
}
```

The sequence DMA does not consume an HDMA channel — the ADC writes to memory
through its own AHB writer. I had reserved a channel for it during planning and did
not need it.

## "Converted" and "in the buffer" are different events

The completion interrupt I fought to get is not in the firmware any more. Sixteen
ISRs per scan, roughly 240,000 a second, each doing nothing but setting a flag, is
worse than reading the status register directly. Then the flag went too, because it
answers the wrong question. `SEQ_CMPT` means the last channel finished *converting*,
not that its value has crossed the bus into the DMA buffer. At `-O0` the code
between the flag and the read was slow enough to hide the gap. At `-O2` it was not, and the last element of each sequence — `ch3` and
`ch7` — started reading the previous step's value. Noise peak-to-peak on those two
cells was 12 and 231 counts against 3 to 9 elsewhere, and since the MUX has already
moved, the stale value belongs to a *different key*. It showed up as the wrong key
registering.

The `cycle_bit` flag in the DMA word looked like the answer and was not: the
software trigger restarts the sequence at element 0, so the pointer never wraps.
After millions of scans all four words still had bit31 clear. So the last slot gets
zeroed before the trigger and watched instead — slots fill in order, and a real DMA
word carries its channel number, so it can never be zero.

`firmware/wish-he/src/hw/driver/keys.c`
([permalink](https://github.com/chcbaram/wish-he/blob/2d5083019c522b35f0fe0d7c4f6d8df51b99d22f/firmware/wish-he/src/hw/driver/keys.c#L1676-L1701))

```c
static inline void keysDmaArm(void)
{
  adc0_buf[KEYS_SEQ_LEN - 1] = 0;
  adc1_buf[KEYS_SEQ_LEN - 1] = 0;
}

static inline bool keysWaitDma(void)
{
  uint32_t spin = 0;

  while (adc0_buf[KEYS_SEQ_LEN - 1] == 0 || adc1_buf[KEYS_SEQ_LEN - 1] == 0)
  {
    if (++spin > KEYS_WAIT_LIMIT)
    {
      timeout_cnt++;
      return false;
    }
  }
  return true;
}
```

Usually that is one comparison. The DMA write cannot happen before the conversion
ends, so waiting on the later event already covers the earlier one; dropping the
`SEQ_CMPT` poll saved 4.5 us per scan on its own. The buffers also have to be
`volatile`: `ATTR_PLACE_AT_NONCACHEABLE_BSS` was already on them, but that is about
the hardware cache, not the compiler.

## Filling the dead time

Conversion is 2.96 us per step and the CPU used to spin through all of it, then
spend 0.93 us processing. Triggering step N and processing step N-1 inside that
wait hides the processing entirely. The next trigger overwrites the DMA buffer, so
the eight words are copied out first — far cheaper than what they hide.

![The conversion takes the same 2.96 us either way. Moving the processing inside that wait saves 0.93 us on every one of the eight steps](dead-time.svg)

`firmware/wish-he/src/hw/driver/keys.c`
([permalink](https://github.com/chcbaram/wish-he/blob/2d5083019c522b35f0fe0d7c4f6d8df51b99d22f/firmware/wish-he/src/hw/driver/keys.c#L2862-L2893))

```c
gpio_write_port(HPM_GPIO0, KEYS_MUX_GPIO_PORT, mux_addr[step]);
keysSettle();

keysDmaArm();                     /* blank the last slot */

adc16_trigger_seq_by_sw(HPM_ADC0);
adc16_trigger_seq_by_sw(HPM_ADC1);

/* everything from here until the conversion ends is free time */
if (has_hold)
{
  for (uint32_t i = 0; i < KEYS_CH_MAX; i++) keysFilter(hold, i, snap[i]);
  if (is_calibrated) keysTrack(hold);
}

if (keysWaitDma() == false)
{
  ret      = false;
  has_hold = false;
  break;
}

/* next address before copying out — its settling overlaps the copy */
gpio_write_port(HPM_GPIO0, KEYS_MUX_GPIO_PORT, mux_addr[step + 1]);

for (uint32_t i = 0; i < KEYS_SEQ_LEN; i++)
{
  snap[i]                = adc0_buf[i];
  snap[KEYS_SEQ_LEN + i] = adc1_buf[i];
}
```

Only the order changes. The ADC configuration and the noise stay where they were.

## The budget

Before that reordering a full scan measured 32.5 us, of which 23.72 us was
conversion and DMA arrival — hardware time the loop cannot touch. The last figure I
measured, on wish61-he, is 26 us per scan and 37,494 scans per second. USB polls at
125 us for 8 kHz, so the scan sits well inside its budget. That is why it can
free-run and let the USB completion callback send the latest values.

The one ADC-side knob I did move is the clock divider. ADC clock is AHB0 (133 MHz)
over that divider, and a conversion takes `sample_cycle + 21` clocks. I measured
all three candidates on 2026-08-17:

| div | ADC clock | conversion | scan | noise p-p (mean / max) |
|---|---|---|---|---|
| 4 | 33.3 MHz | 23.75 us | 29 us | 47 / 55 |
| 3 | 44.4 MHz | 19.12 us | 26 us | 42 / 53 |
| 2 | 66.7 MHz | 14.50 us | 25 us | 47 / 63 |

Going from 4 to 3 made the scan 13 % faster *and* the noise 11 % lower. Going to 2
bought almost nothing and made the worst case worse, which reads like the SAR
running out of settling margin — and 66.7 MHz is past the ~56 MHz that the
published 12-bit 4 MSPS figure implies, while 44.4 MHz keeps 26 % of margin.

## The noise floor is not mine to fix

I widened the sample aperture from 5 to 16 cycles and measured 60 seconds twice,
about 1.5 million scans. Peak-to-peak noise was 47 both times and the scan got
34 % slower for nothing, so the floor is not sample-and-hold settling or source
impedance.

The next suspect was the LEDs, since 83 of them share the board's power:

| LED load | noise p-p |
|---|---|
| off | 39 |
| white 3 % (~156 mA) | 39 |
| white 6 % (~312 mA) | 39 |

It does not move, so it is not power coupling. There was no timed run behind those
three rows, unlike the 60 s aperture test — the peak-to-peak figure is live, so
switching the LEDs on either moves it or it does not, and it did not. What is left is the sensor's own 1/f
flicker noise: the white component averages away across scans, but 1/f has a long
correlation time and an 84 us window does not touch it. That matches the measured
correlation of 0.45 between consecutive scans, where white noise alone would
predict 0.07.

![Correlation against sample spacing. Three points sit on the model; the measured 0.45 sits far above it, and that gap is the 1/f component](noise-correlation.svg)

Averaging shows the same thing from the other side. Summing the last three samples
should improve noise by √3 = 1.73x; measured, it improved by 1.31x. I keep a sum
rather than a mean: dividing by three puts the scale back at 12 bits and quantises
the improvement away, while the sum runs 0 to 12285, about 13.6 effective bits. It
is a *moving* sum, updated each scan by subtracting the oldest sample and adding
the new one, so the decision rate does not drop to a third.

Peak-to-peak 39 is this hardware's floor, and more accumulation does not scale
past it.

![Live depth in the configurator. Every key carries its own press and release points, and the values update while a key is held](via-press-point.png)

## Counts, not millimetres

Nothing in this layer knows about distance. On my board an unpressed cell reads
between 7,474 and 8,383 on the accumulated scale, and a full stroke is about 2,514
counts averaged over 61 keys. Those numbers come out of this board's analog path
and have no reason to match anyone else's instrument. Every decision is made on the
*difference* from a per-key running baseline, with a deadband of 12 counts to keep
the ripple out — a change larger than the band shows up in the same sample, so the
deadband costs no lag.

Turning that difference into millimetres needs the switch's flux-versus-distance
curve and a per-key measured stroke. That is the next post; the press decision
comes after it. The configurator already carries the far end of it — a switch
table with a total travel and two flux figures per entry, and a slot for typing in
a switch nobody has listed yet.

![A listed switch: total travel and the two flux figures the curve is built from](via-switch-type-crop.png)

![The same fields, empty, for a switch that is not in the table](via-custom-switch-crop.png)

![`keys dump` prints the raw count for all 64 cells, eight MUX steps down by eight ADC channels across, with the scan time on the last line](keys-dump-w480.png)

## Still open

- The ADC is configured for `adc16_res_12_bits`, but results arrive spread over the
  full 16-bit range (roughly 42,000 to 46,000), so the code shifts right by 4. I
  still do not know what the resolution setting actually changes.
- The 4 MSPS margin above is back-calculated from published throughput; I could not
  get the original datasheet's maximum ADC input clock.
- The 10.6 us correlation time comes from the datasheet for the Hall sensors on this
  board, not from my own instruments. It carries weight: the whole 1/f argument is a
  comparison against what that figure predicts.

![A USB power meter inline with the board. Everything in the current budget — the MCU, 64 Hall sensors that are never switched off, and whatever the LEDs are drawing — arrives through this one cable](usb-meter-w600.jpg)

## Links

- [wish-he](https://github.com/chcbaram/wish-he)
- [A Ghost Input Above the Actuation Point, and the Two Bugs Under It](../wish-he-rapid-trigger/)
- [Firmware development notes](https://github.com/chcbaram/wish-he/tree/2d5083019c522b35f0fe0d7c4f6d8df51b99d22f/firmware/wish-he/docs) (Korean)

<!--
sources (commit 2d5083019c522b35f0fe0d7c4f6d8df51b99d22f):
- firmware/wish-he/docs/05-adc-scan.md — 스캔 구조, SEQ_INT_EN/CONT_EN 함정, 그레이
  코드, 폴링 전환, 잡음 바닥(LED 흔들기), 눈금은 절대값이 아니다, 남은 것(12비트 설정)
- firmware/wish-he/docs/12-scan-speed.md — 단계별 분해 표(32.5us), "변환 끝 != 버퍼에
  앉음", volatile, cycle_bit 을 못 쓴 이유
- firmware/wish-he/docs/00-hardware.md — 핀맵, ADC 채널 회전, PIOC ALT3, 세틀링,
  8kHz 125us 폴링, LED 83개
- firmware/wish-he/docs/13-rapid-trigger.md — 처리를 변환 대기에 숨기기(2.96/0.93us),
  3개 이동합 1.31배(이론 1.73), 상관계수 0.45 vs 0.07, 1/f
- README.md (보드 표: WISH60 HE 7U 63키 / WISH61 HE 61키), firmware/wish-he/docs/README.md
- firmware/wish-he/src/hw/driver/keys.c — L51-54 mux_addr, L1505-1545 adc_clk_div 표와
  샘플 조리개 실측, L1584-1596 시퀀스 설정, L1676-1701 DMA 센티널, L1710-1728 이동합과
  데드밴드(KEYS_DEADBAND 12, KEYS_ACC_CNT 3), L2862-2893 스캔 루프
- 26us / 37,494 scans/s 는 issues/002-rapid-trigger-ghost-input.md 의 굽기 후 표
  (wish61-he 실측)
- commits: 2c1958e (ADC 클럭 44.4MHz), 692f56c (잡음 출처 분리)
- 그림 없음: docs/images/keys-pipeline.svg 는 06-key-decision.md(아직 안 쓴 "키 판정"
  글)의 그림이고 ⑤ 판정 단계와 스트로크 그래프까지 들어 있어 이 글 몫이 아니다.
  이 글에 맞는 그림은 저장소에 없어 image 를 비우고 사진 자리로 대신했다.
- keys.c 발췌의 주석은 한국어 원본을 영어로 옮기거나 지웠다. 코드 줄은 그대로다
  (네 블록 전부 원본과 한 줄씩 대조했다). L1682-1701 에서는 시험용 강제 실패
  (keysInjectFail) 블록을 뺐다 — 30줄 제한과 주제 때문이다.
-->
