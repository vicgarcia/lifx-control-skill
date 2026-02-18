---
name: lifx-control-skill
description: Control LIFX smart bulbs on the local network. Use when the user wants to control lights, change colors, adjust brightness, or manage smart lighting. Supports discovery, power control, and HSBK color settings via direct LAN protocol.
compatibility: Requires 'lifx' CLI tool installed in PATH (https://github.com/vicgarcia/lifx.py)
metadata:
  author: vic garcia
  version: "2.0"
---

# LIFX Smart Bulb Control

Control LIFX bulbs on the local network using the `lifx` CLI tool.

## Commands

### Discover
```bash
lifx list
# Output: NAME, IP, MAC, MODEL, POWER, COLOR (HSBK values)
```

### Power
```bash
lifx on --label "Name"
lifx off --label "Name"
lifx on --label "Name" --duration 1000   # with transition (ms)
```

### Set Color/Brightness
```bash
lifx set --label "Name" --brightness 32768
lifx set --label "Name" --hue 43690 --saturation 65535 --brightness 52428 --kelvin 4000
lifx set --label "Name" --brightness 65535 --duration 2000
```

Target lights by:
- `--label "Name"` — display name (case-insensitive, from `lifx list`)
- `--ip 192.168.x.x` — IP address
- `--mac xx:xx:xx:xx:xx:xx` — MAC address

## HSBK Color Model

| Property | Range | Notes |
|----------|-------|-------|
| Hue | 0-65535 | ~182 units/degree. 0=red, 10922=yellow, 21845=green, 32768=cyan, 43690=blue, 49151=purple, 54613=magenta |
| Saturation | 0-65535 | 0=white, 65535=full color |
| Brightness | 0-65535 | 655=1%, 6554=10%, 16384=25%, 32768=50%, 65535=100% |
| Kelvin | 2500-9000 | Color temp (visible at low saturation). 2500=warm, 9000=cool |
