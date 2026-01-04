# Context for Claude

## What This Is

A single-file CLI tool for controlling LIFX smart bulbs over LAN. Built with a vibe-coded approach for low-stakes personal use. The entire production tool is [lifx.py](lifx.py) - one file, PEP 723 inline deps, copy-and-run.

## Architecture

- **lifx.py**: The complete tool. Uses PEP 723 inline script metadata so uv handles all dependencies automatically. Can be copied anywhere and just works.
- **lifx_test.py**: Full test suite (26 tests). Uses pytest.
- **first-attempt.ipynb**: Jupyter playground for experimentation.

## The Vibe

Keep it simple. This is a personal tool for controlling lightbulbs, not production infrastructure. If someone asks for a feature, implement it if it's straightforward. If it adds complexity or state management, probably not.

The goal is to keep the whole thing understandable in one sitting. No abstractions for the sake of abstractions. No frameworks. Just functions and a CLI parser.

## Development Workflow

```bash
# Setup
uv venv
source .venv/bin/activate
uv pip install lifxlan pytest

# Test changes
pytest lifx_test.py -v
./lifx.py list

# Update tests when adding features
# Keep coverage high but don't be annoying about it
```

## Design Principles

1. **Single file**: Everything stays in lifx.py. No modules, no packages.
2. **PEP 723**: Production uses inline deps. Dev uses venv. Both work.
3. **Individual bulb control**: No groups. Compose via shell scripts.
4. **Unix philosophy**: Do one thing well. Compose with other tools.
5. **No state**: No config files, no databases, no caching between runs.
6. **Direct LAN protocol**: No cloud, no API keys, no accounts.

## Common Tasks

### Adding a new command
1. Add command function (cmd_something)
2. Add subparser in main()
3. Add tests in lifx_test.py
4. Keep it simple

### Testing
```bash
pytest lifx_test.py -v
```

All tests use mocks - no real bulbs needed for development.

## What Not to Do

- Don't add configuration files
- Don't add databases or persistent state
- Don't add web interfaces or APIs
- Don't break it into multiple files
- Don't add dependencies beyond lifxlan

## The PEP 723 Magic

The shebang and inline metadata at the top of lifx.py tell uv what Python version and dependencies are needed. When you run it via `uv run --script lifx.py`, uv creates an isolated environment automatically. First run takes ~3s, subsequent runs are instant.

This means users can copy one file and run it without any installation process. No pip, no venv management, no requirements.txt. That's the whole point.

## LIFX Protocol Notes

HSBK color model (all raw values):
- Hue: 0-65535 (color wheel, where 65535/360 ≈ 182 per degree)
- Saturation: 0-65535 (color intensity, 0=white, 65535=full color)
- Brightness: 0-65535 (light intensity)
- Kelvin: 2500-9000 (color temperature, only visible at low saturation)

We use raw LIFX values so you can replicate exactly what the bulb displays.

## Git Stuff

Keep commit messages casual but clear. This is a personal project, not corporate code.
