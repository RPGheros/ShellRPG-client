<!-- ShellRPG Comment Banner | Revisionsänderung: Start-/Windows-/Timezone-Fix -->
[Deutsch](README.md) | English

🏛️☠️🌿                                                                 🌿☠️🏛️
╔══════════════════════════════════════════════════════════════════════════════╗
║  _/\______________________________________________________________/\\_     ║
║  \_/\\                                                            /\_/     ║
║  /_/\\   U N R O L L E D   S C R O L L                            /\_\     ║
║  \_\/____________________________________________________________\/_/     ║
╚══════════════════════════════════════════════════════════════════════════════╝
# ShellRPG-client · v0.7.6

## 1. Description

**Artifact role:** Public terminal client for ShellRPG with shell input, status line, event log, map view, standalone mode, and media fallbacks.

**Purpose:** This artifact is meant for direct interaction in Bash, Zsh, PowerShell, or compatible terminals. It sends commands to the server and renders the response in a shell-friendly interface.

**Connected artifacts:**
- `ShellRPG-server` is the authoritative data source.
- `ShellRPG-www` is the graphical sibling client for the same server state.
- `ShellRPG-wiki` explains commands, systems, and terminology for players.

**Governance:** `CLIENT-PUBLIC`

## 2. Dependencies

- Python 3.11 or newer
- pip
- a running `ShellRPG-server` is recommended
- Truecolor/ANSI optional with simpler fallback rendering

## 3. Installation

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell
# Alternativ in CMD: .venv\Scripts\activate.bat
# Alternativ in Bash/Zsh: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m shellrpg_client
```

Standalone mode:
```bash
python -m shellrpg_client --standalone
```

## 4. Feedback & Contribution

Feedback should always mention the terminal profile, operating system, and executed command.
Contribution is welcome as long as shell integrity, fallback behavior, and public/private separation remain intact.
UI changes should stay understandable in both German and English where applicable.

🏛️🌿☠️══════════════════════════════════════════════════════════════☠️🌿🏛️
