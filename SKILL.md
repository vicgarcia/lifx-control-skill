---
name: lifx-lighting-control
description: Control LIFX smart bulbs on the local network. Use when the user wants to control lights, change colors, adjust brightness, or manage smart lighting. Supports discovery, power control, and HSBK color settings via direct LAN protocol.
compatibility: Requires uv (Python package manager) and network access to LIFX bulbs on local LAN.
metadata:
  author: vic garcia
  version: "1.0"
---

# LIFX Smart Bulb Control

This skill enables control of LIFX smart bulbs on the local network using the `scripts/lifx.py` CLI tool.

## Prerequisites

- **uv** must be installed (Python package manager)
- LIFX bulbs must be on the same local network
- No cloud accounts or API keys needed - uses direct LAN protocol

## Behavior

**Execute commands directly**—don't explain CLI usage or give instructions. When the user asks to control lights, run the commands and report the results. Only explain CLI usage if the user explicitly asks how the tool works.

## How to Use

The CLI tool is located at `scripts/lifx.py` in this skill's directory. Run commands using:

```bash
uv run --script scripts/lifx.py <command> [options]
```

First run takes ~3 seconds to set up dependencies. Subsequent runs are instant.

## Commands

### Discover lights

List all LIFX bulbs on the network:

```bash
uv run --script scripts/lifx.py list
```

Output shows: NAME, IP, MAC, MODEL, POWER, COLOR (HSBK values)

### Turn lights on/off

```bash
# By label (name)
uv run --script scripts/lifx.py on --label "Office"
uv run --script scripts/lifx.py off --label "Bedroom"

# By IP address
uv run --script scripts/lifx.py on --ip 192.168.1.100

# By MAC address
uv run --script scripts/lifx.py off --mac d0:73:d5:xx:xx:xx

# With transition duration (milliseconds)
uv run --script scripts/lifx.py on --label "Office" --duration 1000
```

### Set color and brightness

Use `set` command with HSBK values. You can set any combination of properties:

```bash
# Set brightness only (50%)
uv run --script scripts/lifx.py set --label "Desk" --brightness 32768

# Set hue only (keeps other properties)
uv run --script scripts/lifx.py set --label "Desk" --hue 21845

# Set full color
uv run --script scripts/lifx.py set --label "Desk" --hue 43690 --saturation 65535 --brightness 52428 --kelvin 4000

# With transition
uv run --script scripts/lifx.py set --label "Office" --brightness 65535 --duration 2000
```

### Rename a light

```bash
uv run --script scripts/lifx.py rename --label "Old Name" "New Name"
```

## HSBK Color Model

LIFX uses raw 16-bit values (0-65535) for color:

| Property | Range | Description |
|----------|-------|-------------|
| **Hue** | 0-65535 | Color wheel position. ~182 units per degree. 0=red, 21845=green, 43690=blue |
| **Saturation** | 0-65535 | Color intensity. 0=white/no color, 65535=full color |
| **Brightness** | 0-65535 | Light intensity. 0=dim, 65535=full brightness |
| **Kelvin** | 2500-9000 | Color temperature. Only visible at low saturation. 2500=warm, 9000=cool |

### Common Colors Reference

| Color | Hue | Saturation | Notes |
|-------|-----|------------|-------|
| Red | 0 | 65535 | |
| Orange | 5461 | 65535 | |
| Yellow | 10922 | 65535 | |
| Green | 21845 | 65535 | |
| Cyan | 32768 | 65535 | |
| Blue | 43690 | 65535 | |
| Purple | 49151 | 65535 | |
| Magenta | 54613 | 65535 | |
| Warm White | any | 0 | Use Kelvin 2500-3000 |
| Cool White | any | 0 | Use Kelvin 5000-6500 |

### Brightness Levels

| Percentage | Raw Value |
|------------|-----------|
| 100% | 65535 |
| 75% | 49151 |
| 50% | 32768 |
| 25% | 16384 |
| 10% | 6554 |
| 1% | 655 |

## Identifying Lights

Always run `list` first to discover available lights and their identifiers:

```bash
uv run --script scripts/lifx.py list
```

You can then target lights by:
- `--label "Name"` - The display name (case-insensitive)
- `--ip 192.168.x.x` - IP address
- `--mac d0:73:xx:xx:xx:xx` - MAC address

## Composing Complex Behaviors

Chain multiple commands for complex operations:

```bash
# Turn on and set to warm dim
uv run --script scripts/lifx.py on --label "Bedroom" && \
uv run --script scripts/lifx.py set --label "Bedroom" --brightness 6554 --saturation 0 --kelvin 2700

# Set multiple lights
for light in "Office" "Desk" "Hallway"; do
  uv run --script scripts/lifx.py set --label "$light" --brightness 32768
done
```

## Troubleshooting

- **"No LIFX lights found"**: Ensure bulbs are powered on and connected to the same network
- **"Light not found"**: Run `list` to verify the light's current label/IP/MAC
- **Slow discovery**: Use `-n` flag if you know the number of lights: `scripts/lifx.py -n 3 list`
