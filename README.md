I wanted a simple CLI tool to mess with my LIFX lightbulbs, which I usually control via Apple HomeKit. I've been having success generating small, low-stakes tools with Claude Code, taking a pretty vibe-coded approach to things that don't need to be perfect. This is one of those things.

The whole tool is a single Python file using PEP 723 inline dependencies and uv. No package management, no versioning, no installation hassle. Just a drop-in file that works. You copy it somewhere, run it, and you're controlling lights. That's the entire onboarding.

## Installation

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy the script to somewhere in your PATH
cp lifx.py ~/.local/bin/lifx
chmod +x ~/.local/bin/lifx

# Make sure ~/.local/bin is in your PATH
export PATH="$HOME/.local/bin:$PATH"

# Done
lifx list
```

First run takes ~3 seconds while uv handles dependencies. After that it's instant.

## Usage

```bash
# First, see what's on your network
lifx list
# NAME           IP              MAC                MODEL       POWER  COLOR
# bulb_a1b2c3    192.168.1.100   d0:73:d5:a1:b2:c3  LIFX A19    On     HSBK(...)
# bulb_x7y8z9    192.168.1.101   d0:73:d5:x7:y8:z9  LIFX A19    Off    HSBK(...)

# Give them better names (use MAC since default names are less helpful)
lifx rename --mac d0:73:d5:a1:b2:c3 "Office"
lifx rename --mac d0:73:d5:x7:y8:z9 "Bedroom"

# Now turn on and off
lifx on --label "Office"
lifx off --label "Bedroom"

# Set colors and brightness (raw LIFX values: Hue/Sat/Brightness 0-65535, Kelvin 2500-9000)
lifx set --label "Office" --hue 43690 --saturation 65535 --brightness 52428 --kelvin 4000
lifx set --mac d0:73:d5:x7:y8:z9 --hue 6371 --saturation 39321 --brightness 32768 --kelvin 2700

# Adjust just brightness (other properties stay the same)
lifx set --label "Office" --brightness 65535
lifx set --mac d0:73:d5:x7:y8:z9 --brightness 19660
```

## Common Colors (Hue values)

Red: `--hue 0`
Orange: `--hue 6371` (~35°)
Yellow: `--hue 10923` (~60°)
Green: `--hue 21845` (~120°)
Cyan: `--hue 32768` (~180°)
Blue: `--hue 43690` (~240°)
Purple: `--hue 50972` (~280°)
Pink: `--hue 54613` (~300°)

Saturation at 65535 gives you full color, lower values wash it out toward white. Kelvin only matters when saturation is low.

## Development

```bash
# Set up a virtual environment
uv venv
source .venv/bin/activate
uv pip install lifxlan pytest

# Run tests
pytest lifx_test.py -v

# Test
./lifx.py list
```

## License

Do whatever you want with this.
