I wanted a simple CLI tool to mess with my LIFX lightbulbs, which I usually control via Apple HomeKit. I've been having success generating small, low-stakes tools with Claude Code, taking a pretty vibe-coded approach to things that don't need to be perfect. This is one of those things.

The whole tool is a single Python file using PEP 723 inline dependencies and uv. No package management, no versioning, no installation hassle. Just a drop-in file that works. You copy it somewhere, run it, and you're controlling lights. That's the entire onboarding.

## Installation

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Copy the script somewhere in your PATH, make it executable, and call it directly:

```bash
cp scripts/lifx.py ~/.local/bin/lifx
chmod +x ~/.local/bin/lifx

# Make sure ~/.local/bin is in your PATH
export PATH="$HOME/.local/bin:$PATH"

# Now use it
lifx list
```

### Option 2: Run via uv

Run the script through uv without installing:

```bash
uv run --script scripts/lifx.py list
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

## HSBK Color Model

LIFX uses raw 16-bit values (0-65535) for color:

| Property | Range | Description |
|----------|-------|-------------|
| **Hue** | 0-65535 | Color wheel position. ~182 units per degree. |
| **Saturation** | 0-65535 | Color intensity. 0=white, 65535=full color |
| **Brightness** | 0-65535 | Light intensity. 0=dim, 65535=full brightness |
| **Kelvin** | 2500-9000 | Color temperature. Only visible at low saturation. 2500=warm, 9000=cool |

### Common Colors (Hue values)

Red: `--hue 0`
Orange: `--hue 6371` (~35°)
Yellow: `--hue 10923` (~60°)
Green: `--hue 21845` (~120°)
Cyan: `--hue 32768` (~180°)
Blue: `--hue 43690` (~240°)
Purple: `--hue 50972` (~280°)
Pink: `--hue 54613` (~300°)

Saturation at 65535 gives you full color, lower values wash it out toward white. Kelvin only matters when saturation is low.

## Agent Skill

This repo is an [Agent Skill](https://agentskills.io) that gives AI coding agents the ability to control LIFX lights.

### Installation

**Important**: The directory name must match the skill name. Rename the directory to `lifx-lighting-control`:

```bash
# Clone and rename
git clone https://github.com/vicgarcia/lifx-lighting-control.git

# Or if already cloned with a different name
mv lifx-spike lifx-lighting-control
```

Then add the skill to your agent. For Claude Code:

```bash
claude /install-skill /path/to/lifx-lighting-control
```

### What the agent can do

Once installed, you can ask your agent to:
- "Turn on the office light"
- "Set the bedroom to a warm dim glow"
- "Make the desk lamp blue at 50% brightness"
- "List all lights on my network"

The agent uses `scripts/lifx.py` via bash commands to control the lights.

## Development

### Architecture

- **scripts/lifx.py**: The complete tool. Single file with PEP 723 inline deps.
- **lifx_test.py**: Test suite (26 tests). All mocked, no real bulbs needed.
- **SKILL.md**: Agent skill definition for AI coding assistants.
- **first-attempt.ipynb**: Jupyter playground for experimentation.

### Setup

```bash
uv venv
source .venv/bin/activate
uv pip install lifxlan pytest

# Run tests
pytest lifx_test.py -v

# Test against real bulbs
./scripts/lifx.py list
```

### Design Principles

1. **Single file**: Everything stays in scripts/lifx.py. No modules, no packages.
2. **PEP 723**: Uses inline script metadata so uv handles dependencies automatically.
3. **Individual bulb control**: No groups. Compose via shell scripts.
4. **Unix philosophy**: Do one thing well. Compose with other tools.
5. **No state**: No config files, no databases, no caching between runs.
6. **Direct LAN protocol**: No cloud, no API keys, no accounts.

### Adding a new command

1. Add command function (cmd_something)
2. Add subparser in main()
3. Add tests in lifx_test.py
4. Keep it simple

### What not to do

- Don't add configuration files
- Don't add databases or persistent state
- Don't add web interfaces or APIs
- Don't break it into multiple files
- Don't add dependencies beyond lifxlan

## License

Do whatever you want with this.
