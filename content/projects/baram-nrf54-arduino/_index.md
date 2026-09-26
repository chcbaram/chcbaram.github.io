---
title: "baram-nrf54-arduino"
description: "An Arduino core for the Nordic nRF54L series, built so existing Adafruit Bluefruit (nRF52) sketches keep working."
repo: "https://github.com/chcbaram/baram-nrf54-arduino"
---

An Arduino core for the Nordic nRF54L series. The goal is that sketches written
for Adafruit's nRF52 Bluefruit core keep working, so the API follows Bluefruit
rather than inventing its own.

As of 0.4.0 the peripheral APIs (`Wire`, `SPI`, `attachInterrupt`, `analogWrite`,
`analogRead`) are verified on hardware across four boards, and BLE works in both
peripheral and central roles. There is no bootloader yet — uploading needs SWD.

One thing that differs from nRF52: on nRF54L a peripheral is tied to a GPIO port,
so a wrong pin assignment fails the build instead of failing silently at runtime.
