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

**Artifact role:** Public terminal client for ShellRPG with shell input, status line, event log, map view, and media fallbacks.

**Purpose:** This artifact is meant for direct interaction in Bash, Zsh, PowerShell, or compatible terminals. It sends commands to the server and renders the response in a shell-friendly interface.

**Connected artifacts:**
- `ShellRPG-server` is the authoritative data source.
- `ShellRPG-www` is the graphical sibling client for the same server state.
- `ShellRPG-wiki` explains commands, systems, and terminology for players.

**Governance:** `CLIENT-PUBLIC`

## Maintenance Note

- For relevant content, contract, feature, or editorial changes touching this
  endpoint, update `README.md`, `README.en.md`, and `VERSION` together.

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

The dedicated browser surface is provided separately by `ShellRPG-www`.
The terminal client keeps its own local media previews; WWW image delivery is
handled separately through the web/CDN path.

Current canon preparation:
- future UI text must distinguish monster, hive, wildlife, nature, and demons
  more clearly
- equipment rendering is being prepared for six ring slots per character
- when the server delivers redacted tile world hints, the map view now shows
  a `Milieu: ...` line below the map instead of inventing a separate
  client-only terminology path
- the same map contract can now also surface a redacted urban hint from
  `urban_suspicion_line`; the terminal client stays bound to the
  server-provided public contract instead of inventing local suspicion logic
- the same contract can now also surface a redacted urban diagnosis from the
  persisted urban suspicion pool; tile hint and diagnosis stay bound to the
  same server-side registry refs
- the terminal client now also ships a local `matrix` command tree for
  `/api/matrix/health` and `/api/matrix/status`, so the same severity,
  conflict, hotspot, and peer diagnostics can be inspected in a shell-
  friendly view
- the same matrix path can now also filter character conflicts locally
  (`matrix conflicts <filter>`) and drill down by character name,
  `conflict_id`, or `field_conflict_id` (`matrix inspect <...>`)
- the drilldown shows preferred, fallback, and merged previews, merge
  mode, winner side, and prioritized delta reasons directly inside the
  terminal output instead of only rendering the short conflict list
- the same matrix health is now also surfaced as a compact `Mx:` hint in
  the live HUD line without displacing the shell prompt or the actual game
  snapshot

## 4. Feedback & Contribution

Feedback should always mention the terminal profile, operating system, and executed command.
Contribution is welcome as long as shell integrity, fallback behavior, and public/private separation remain intact.
UI changes should stay understandable in both German and English where applicable.

🏛️🌿☠️══════════════════════════════════════════════════════════════☠️🌿🏛️
