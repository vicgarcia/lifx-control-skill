# lifx-control-skill

A skill that gives AI coding agents the ability to control LIFX smart bulbs over your local network.

## What it does

Once installed, you can ask your agent things like:
- "Turn on the office light"
- "Set the bedroom to a warm dim glow"
- "Make the desk lamp blue at 50% brightness"
- "List all lights on my network"

The agent controls your lights directly via LAN protocol—no cloud accounts, no API keys, no internet required.

## Requirements

- [lifx CLI tool](https://github.com/vicgarcia/lifx.py) installed and available in PATH
- LIFX bulbs on the same local network

## Installation

### 1. Install lifx CLI tool

First, install the `lifx` command-line tool:

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Download and install lifx
mkdir -p ~/.local/bin
curl -fsSL https://raw.githubusercontent.com/vicgarcia/lifx.py/main/lifx -o ~/.local/bin/lifx
chmod +x ~/.local/bin/lifx

# Ensure ~/.local/bin is in your PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
lifx --help
```

For detailed installation instructions, see: https://github.com/vicgarcia/lifx.py

### 2. Install the skill

Clone this skill to your Claude Code skills directory:

```bash
git clone https://github.com/vicgarcia/lifx-control-skill.git ~/.claude/skills/lifx-control-skill
```

Or for pi-coding-agent:

```bash
git clone https://github.com/vicgarcia/lifx-control-skill.git ~/.pi/agent/skills/lifx-control-skill
```

## How it works

The skill provides instructions to the agent on how to use the `lifx` command-line tool. The agent reads [SKILL.md](SKILL.md) to understand available commands and executes them via bash.

The `lifx` tool communicates directly with LIFX bulbs over your local network using the [lifxlan](https://github.com/mclarkk/lifxlan) library.

## Usage Examples

Once installed, your agent can execute commands like:

```bash
# Discover all lights
lifx list

# Turn on by name
lifx on --label "Office"

# Set color and brightness
lifx set --label "Desk" --hue 43690 --saturation 65535 --brightness 32768

# Turn off
lifx off --label "Bedroom"
```

See [SKILL.md](SKILL.md) for complete documentation on available commands and the HSBK color model.
