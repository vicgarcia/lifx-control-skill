# lifx-lighting-control

A skill that gives AI coding agents the ability to control LIFX smart bulbs over your local network.

## What it does

Once installed, you can ask your agent things like:
- "Turn on the office light"
- "Set the bedroom to a warm dim glow"
- "Make the desk lamp blue at 50% brightness"
- "List all lights on my network"

The agent controls your lights directly via LAN protocol—no cloud accounts, no API keys, no internet required.

## Requirements

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- LIFX bulbs on the same local network

## Installation

Clone to your Claude Code skills directory:

```bash
git clone https://github.com/vicgarcia/lifx-lighting-control.git ~/.claude/skills/lifx-lighting-control
```

## How it works

The skill uses a single Python script (`scripts/lifx.py`) that communicates directly with LIFX bulbs over your local network using the [lifxlan](https://github.com/mclarkk/lifxlan) library. The agent reads `SKILL.md` to understand available commands and executes them via bash.

## CLI Tool

The `scripts/lifx.py` script works great on its own if you want to control lights from the command line.

### Install

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy to your PATH and make executable
cp scripts/lifx.py ~/.local/bin/lifx
chmod +x ~/.local/bin/lifx

# Make sure ~/.local/bin is in your PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Usage

```bash
# Discover lights
lifx list

# Power control
lifx on --label "Office"
lifx off --label "Bedroom"

# Set colors (raw LIFX values: H/S/B 0-65535, Kelvin 2500-9000)
lifx set --label "Office" --hue 43690 --saturation 65535 --brightness 52428
lifx set --label "Bedroom" --brightness 16384 --saturation 0 --kelvin 2700

# Rename lights
lifx rename --mac d0:73:d5:a1:b2:c3 "Office"
```

### Common Colors

| Color | Hue |
|-------|-----|
| Red | 0 |
| Orange | 6371 |
| Yellow | 10923 |
| Green | 21845 |
| Cyan | 32768 |
| Blue | 43690 |
| Purple | 50972 |
| Pink | 54613 |

Saturation at 65535 = full color, 0 = white. Kelvin only matters at low saturation.
