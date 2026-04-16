# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

**textUtilsBot** is a Telegram bot that provides inline query handlers for text conversion utilities (binary/hex/base64 encoding, typography, URL encoding, language layout switching, currency calculations, etc.). It uses Telegram's inline query interface and is built on Python async (aiotg/aiohttp).

## Commands

Run all commands from the project root (no `PYTHONPATH` needed).

```bash
# Run tests
pytest

# Run a single test file
pytest tests/test_strconv/test_banner.py

# Run with coverage
coverage run -m pytest && coverage report

# Run the bot (debug/polling mode — set DEBUG=True in config.py)
python -m app.bot

# Docker
docker compose up -d --build
```

**Windows PowerShell:**
```powershell
pytest
python -m app.bot
```

## Setup

```bash
# Create venv and install deps
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # for testing

# Copy and edit config
cp examples/config.py app/data/config.py
# Set TOKEN, HOST, DEBUG=True for local dev
```

## Architecture

### Plugin System for Text Processors

The core design is a dynamic plugin system:

- **`app/txtproc/abc.py`** — Abstract base classes. Every processor extends `TextProcessor` and any combination of mixins:
  - `Universal` — processes any non-empty text
  - `Exclusive` — only one such processor runs if matched (for decoders)
  - `Reversible` — processor has an inverse (for encoders)
  - `HTML` — result may contain HTML (processor must escape input)
  - `PrefixedTextProcessor` — for prefix-based matching (e.g., URLs)

- **`app/txtproc/loader.py`** — Dynamically discovers all `TextProcessor` subclasses in `app/strconv/` via the `__txtproc__` marker.

- **`app/strconv/`** — One file per feature (e.g., `banner.py`, `url.py`, `langlayout.py`). Each file registers itself by defining `__txtproc__ = True` and subclassing `TextProcessor`.

- **`app/bot.py`** — Entry point: wires Telegram events to the processor loader, manages webhook/polling, and runs background tasks (currency rate updates).

### Adding a New Processor

1. Create `app/strconv/myfeature.py` with `__txtproc__ = True` and a class extending `TextProcessor` + appropriate mixins.
2. Add localization keys to `app/localizations.ini`:
   - `hint_my_feature` — short title shown in inline results
   - `help_my_feature` — description shown in help
3. Write tests in `tests/test_strconv/test_myfeature.py`.
4. The processor is auto-discovered on next bot start — no registration needed.

### Other Key Files

| File | Purpose |
|---|---|
| `app/queryutil.py` | Builders for Telegram inline results and keyboard callbacks |
| `app/txtprocutil.py` | Localization helpers, processor description formatting |
| `app/msgdb.py` | SQLite wrapper storing original queries (enables "decrypt" button) |
| `app/data/config.py` | Runtime config (TOKEN, HOST, DEBUG, ports) — not in version control |
| `app/localizations.ini` | All user-facing strings in EN/RU |
| `examples/config.py` | Template for `app/data/config.py` |

### Configuration

`app/data/config.py` holds sensitive values and is gitignored. Key settings:
- `TOKEN` — Telegram bot token
- `HOST` — external hostname for webhook URL
- `DEBUG` — set `True` for polling mode (no webhook required, good for local dev)
- `METRICS_PORT` — Prometheus metrics endpoint (default 8000)

## CI/CD

- `.github/workflows/ci-build.yml` — runs `pytest` on Python 3.10–3.14
- `.github/workflows/publish.yml` — builds and pushes Docker image to `ghcr.io` on version tags (e.g., `v2.4.0`)
- Docker base image: `python:3.14-alpine` (multistage build)
