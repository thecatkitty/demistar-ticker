# Demistar Ticker
**Demistar** (Dynamic Electronic Monitor for Information on Status, Timetable, Attractions and Rooms) is a digital signage system for information about an event schedule. [BT Foundation](https://fundacjabt.eu/) is currently the sole adopter of the system.

This repository contains the firmware of Ticker device, consisting of two 64x8 LED matrices and two concentric NeoPixel rings, connected to the Raspberry Pi Pico W microcontroller board, managed over Wi-Fi using a JSON-based API.

## Connections
- RP - Raspberry Pi Pico W board
- MA - top matrix
- MB - bottom matrix
- RA - outer ring
- RB - inner ring
- JP - 5 V power jack

```
RP GP9  -> RA IN
RP GP13 -> MA CS
RP GP14 -> MA CLK
RP GP15 -> MA DIN
RP GP17 -> MB CS
RP GP18 -> MB CLK
RP GP19 -> MB DIN

RA OUT  -> RB IN
RA VCC  -> RB VCC
RA GND  -> RB GND

JP +5V  -> RP VSYS
        -> MA VCC
        -> MB VCC
        -> RA VCC
JP GND  -> RP GND
        -> MA GND
        -> MB GND
        -> RB GND
```
