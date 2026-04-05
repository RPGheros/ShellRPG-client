# ShellRPG Datei-Banner | Terminal-Client v0.7.6 | Deutsch kommentiert
from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import socket
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover - optionale Komfortabhängigkeit
    psutil = None

from shellrpg_client.api_client import ApiClient
from shellrpg_client.terminal_layout import (
    ReservedRenderSession,
    ReservedTerminalRenderer,
    fit_plain_terminal_line,
    fit_text_width,
    format_shell_prompt,
    pad_text_width,
)
from shellrpg_client.version import RELEASE_VERSION
from shellrpg_client.ui import (
    render_buffs,
    render_city,
    render_combat,
    render_equipment,
    render_inventory,
    render_journal,
    render_map,
    render_market,
    render_quests,
)

HEADER_ROWS = 4
PROFILE_PATH = Path.home() / ".shellrpg-client-profile.json"
GAME_VERBS = {
    "look", "inspect", "walk", "explore", "hunt", "gather", "map", "inventory", "equipment", "buffs", "quests",
    "equip", "use", "read", "book", "lang", "help", "showcommands", "show", "commands", "attack", "guard", "dodge", "cast",
    "auto", "market", "merchant", "buy", "sell", "craft", "socket", "enchant", "brew", "soul", "soulforge",
    "cube", "city", "militia", "garrison", "faction", "npc", "artifact", "rcon", "journal", "trade", "party",
    "quest", "pet", "summon", "townfolk", "server", "recovery", "weather", "weave", "dialogue", "talk", "service",
}
ANSI = "\x1b["
SPINNERS = ["● ○ ○ ○ ○", "● ● ○ ○ ○", "● ● ● ○ ○", "● ● ● ● ○", "● ● ● ● ●"]
CHARACTER_FACTIONS = ["Menschen", "Amazonen", "Waldelfen", "Dryaden", "Baumwesen", "Nekari", "Ssarathi", "Salzlungen", "Orks", "Dämonen"]
CHARACTER_RACES = ["Mensch", "Nekari", "Ssarathi", "Salzlunge", "Waldelf", "Dryade", "Baumwesen"]
CHARACTER_CLASSES = ["Ritter", "Totenbeschwörer", "Kleriker", "Waldläufer", "Magier", "Dieb", "Beastmaster"]
CHARACTER_COMMAND_ALIASES = {"character", "char", "chars"}
CONTROL_COMMAND_ALIASES = {"control", "controller"}
MATRIX_COMMAND_ALIASES = {"matrix"}
OBSERVER_SAFE_COMMAND_PATTERNS = (
    "showcommands",
    "show commands",
    "commands",
    "help",
    "look",
    "inspect",
    "map",
    "inventory",
    "equipment",
    "buffs",
    "quests",
    "quest log",
    "quests log",
    "journal",
    "lang",
    "lang de",
    "lang en",
    "market",
    "merchant",
    "merchant list",
    "brew menu",
    "enchant menu",
    "artifact",
    "artifact weave",
    "artifact weave cities",
    "artifact weave buildings",
    "artifact weave detailed",
    "artifact weave conditions",
    "rcon",
    "rcon status",
    "rcon ticks",
    "rcon savepoint",
    "rcon npcs",
    "rcon weather",
    "rcon recovery",
    "rcon artifact",
    "rcon npc opinion",
    "rcon npc schedule",
    "rcon rumor list",
    "rcon quest inspect",
    "npc",
    "npc menu",
    "city",
    "city status",
    "militia",
    "militia status",
    "garrison",
    "garrison status",
)
INTRO_FRAME_DELAY = 0.18
INTRO_SETTLE_DELAY = 0.28
SCROLL_FRAME_DELAY = 0.09
SCROLL_PANEL_ROWS = 16
PARCHMENT_CODE = "38;5;223"
INK_CODE = "38;5;94"
ACCENT_CODE = "38;5;136"
TITLE_CODE = "38;5;178"
SHADOW_CODE = "38;5;58"
MATRIX_HEALTH_REFRESH_SECONDS = 12.0


# Aktiviert unter Windows nach Möglichkeit ANSI-Escapes für Cursorbewegung und Farben.
def enable_ansi_support() -> None:
    os.system("")


# Liest ein lokales Charakterprofil für Intro und Rejoin aus einer JSON-Datei.
def read_profile() -> dict[str, Any] | None:
    if not PROFILE_PATH.exists():
        return None
    try:
        return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None


# Speichert das lokale Charakterprofil nach der Erstellung oder Änderung in eine JSON-Datei.
def write_profile(profile: dict[str, Any]) -> None:
    PROFILE_PATH.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")


# Gibt einen Text optional mit ANSI-Farbe zurück, wenn die Konsole ANSI versteht.
def color(text: str, code: str) -> str:
    return f"{ANSI}{code}m{text}{ANSI}0m"


# Ermittelt lokal sichtbare Netzwerkschnittstellen, WLAN-Hinweise und harmlose Pseudoprotokolle für den Fake-Boot.
def local_probe_targets() -> list[dict[str, str]]:
    targets: list[dict[str, str]] = []
    host = socket.gethostname()
    targets.append({"kind": "host", "label": host})
    if psutil is not None:
        for name in list(psutil.net_if_addrs().keys())[:6]:
            targets.append({"kind": "adapter", "label": name})
    ssid = ""
    if sys.platform.startswith("win"):
        try:
            result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, timeout=2)
            for line in result.stdout.splitlines():
                low = line.lower().strip()
                if low.startswith("ssid") and "bssid" not in low and ":" in line:
                    ssid = line.split(":", 1)[1].strip()
                    break
        except Exception:
            ssid = ""
    if ssid:
        targets.append({"kind": "ssid", "label": ssid})
    for proto in ["SMB", "FTP", "NFS", "SSH", "SFTP", "HTTP", "HTTPS", "mDNS", "Bluetooth", "RPC"]:
        targets.append({"kind": "proto", "label": proto})
    return targets[:12]


# Ermittelt eine sichere Panelbreite, die nie bis in den letzten Terminal-Viewport hineinragt.
def panel_width_for_columns(columns: int, minimum: int = 36, maximum: int = 76) -> int:
    hard_limit = max(12, columns - 1)
    soft_target = min(maximum, max(12, columns - 6))
    return max(12, min(hard_limit, max(minimum, soft_target)))


# Baut zentrierte Intro-Panels mit ruhigen, vollstaendigen Frames statt mit konkurrierenden Einzelzeichen-Updates.
def build_intro_panel_lines(
    columns: int,
    title: str,
    body_lines: list[str],
    footer: str = "",
    phase_label: str = "INIT",
    rows: int = 12,
) -> list[str]:
    panel_width = panel_width_for_columns(columns, minimum=38, maximum=78)
    inner = max(20, panel_width - 4)
    left_pad = " " * max(0, (columns - panel_width) // 2)
    content_slots = max(4, rows - 4)
    normalized = [pad_text_width(f"[{phase_label}] {title}", inner, "center")]
    normalized.append("")
    normalized.extend(pad_text_width(line, inner) for line in body_lines)
    if footer:
        normalized.append("")
        normalized.append(pad_text_width(footer, inner, "center"))
    normalized = normalized[:content_slots]
    while len(normalized) < content_slots:
        normalized.append(" " * inner)
    lines = [left_pad + color("┌" + "─" * (panel_width - 2) + "┐", ACCENT_CODE)]
    for idx, line in enumerate(normalized):
        code = TITLE_CODE if idx == 0 else (ACCENT_CODE if footer and idx == len(normalized) - 1 else INK_CODE)
        lines.append(left_pad + color("│", ACCENT_CODE) + color(line, code) + color("│", ACCENT_CODE))
    lines.append(left_pad + color("└" + "─" * (panel_width - 2) + "┘", ACCENT_CODE))
    return lines[:rows]


# Rendert eine komplette Intro-Phase gegen einen festen Anker und wartet kontrolliert, bevor die naechste Phase startet.
def render_intro_phase(
    session: ReservedRenderSession,
    columns: int,
    title: str,
    body_lines: list[str],
    footer: str = "",
    phase_label: str = "INIT",
    delay: float = INTRO_FRAME_DELAY,
) -> None:
    current_columns = session.renderer.terminal_size().columns or columns
    session.render(build_intro_panel_lines(current_columns, title, body_lines, footer=footer, phase_label=phase_label))
    time.sleep(delay)


# Führt den atmosphärischen Fake-Boot-Prozess phasenweise aus und hält Intro-Rendering strikt vom Live-HUD getrennt.
def run_fake_boot(skip_intro: bool, renderer: ReservedTerminalRenderer | None = None) -> None:
    if skip_intro:
        return
    active_renderer = renderer or ReservedTerminalRenderer()
    columns = active_renderer.terminal_size().columns
    targets = local_probe_targets()
    probe_labels = []
    for target in targets[:6]:
        verdict = "VERWORFEN" if random.random() < 0.35 else "FEHLSCHLAG"
        probe_labels.append(f"{target['kind'].upper():>7} · {target['label']} · {verdict}")
    glyphs = ["#@$%&*?!/\\|[]{}<>~^_-=", "%&#@?!<>[]{}\\/-=+*"]
    with ReservedRenderSession(active_renderer, rows=12) as session:
        render_intro_phase(
            session,
            columns,
            "ShellRPG Initiation Bootstrap",
            [
                "Das Intro verwendet jetzt nur noch vollstaendige Frames im reservierten Bereich.",
                "Kein Backspace-Typing, kein konkurrierender Prompt-Zugriff, kein flackernder Cursor.",
                "Lokale Ziele werden sondiert, ohne externe Hosts zu beruehren.",
            ],
            footer="Phase 1 von 4 · Synchronisiere Renderzustand",
            phase_label="BOOT",
            delay=INTRO_SETTLE_DELAY,
        )
        render_intro_phase(
            session,
            columns,
            "Lokale Sondierung fehlgeschlagen",
            probe_labels,
            footer="Phase 2 von 4 · Alle lokalen Kanaele bleiben verschlossen",
            phase_label="SCAN",
            delay=INTRO_FRAME_DELAY,
        )
        render_intro_phase(
            session,
            columns,
            "Versuche Zugriff zu erhalten, umgehe Sicherheitsvorschriften.",
            [
                fit_text_width(f"{glyphs[0]}  Integritaetswache aktiviert  {glyphs[1]}", panel_width_for_columns(columns) - 6),
                fit_text_width(f"{glyphs[1]}  Prozess wird geordnet verworfen  {glyphs[0]}", panel_width_for_columns(columns) - 6),
                "Jede Phase schliesst sauber ab, bevor die naechste beginnt.",
            ],
            footer="Phase 3 von 4 · Kein Rendering greift in die Eingabezeile ein",
            phase_label="GLITCH",
            delay=INTRO_SETTLE_DELAY,
        )
        render_intro_phase(
            session,
            columns,
            "Erwachen",
            [
                "Autsch ... was war das?! Was ist gerade passiert?!",
                "Wo bin ich?!",
                "Wer bin ich?!",
            ],
            footer="Phase 4 von 4 · Uebergang in die Charaktererstellung",
            phase_label="AWAKE",
            delay=0.42,
        )


# Baut eine Shell-zeilenfreundliche Eingabeaufforderung fuer Wizards und Schriftrollen-Dialoge.
def format_wizard_prompt(cwd: Path, columns: int, label: str) -> str:
    base_prompt = format_shell_prompt(cwd, columns)
    return fit_text_width(f"{base_prompt}{label}: ", max(1, columns - 1))


# Baut die Schriftrollenoptik fuer die Charaktererstellung in einer festen Hoehe auf.
def build_scroll_panel_lines(
    columns: int,
    title: str,
    subtitle: str,
    entries: list[str],
    footer: str = "",
    reveal_rows: int | None = None,
    rows: int = SCROLL_PANEL_ROWS,
) -> list[str]:
    panel_width = panel_width_for_columns(columns, minimum=40, maximum=74)
    inner = max(12, panel_width - 6)
    left_pad = " " * max(0, (columns - panel_width) // 2)
    content_rows = max(6, rows - 4)
    full_content = [
        ("  " + pad_text_width(title, inner - 2, "center"), TITLE_CODE),
        ("  " + pad_text_width(subtitle, inner - 2, "center"), ACCENT_CODE),
    ]
    for entry in entries:
        full_content.append(("  " + pad_text_width(entry, inner - 2), INK_CODE))
    if footer:
        full_content.append(("  " + pad_text_width(footer, inner - 2, "center"), ACCENT_CODE))
    visible = reveal_rows if reveal_rows is not None else len(full_content)
    visible = max(0, min(content_rows, visible))
    while len(full_content) < content_rows:
        full_content.append((" " * inner, PARCHMENT_CODE))
    lines = [
        left_pad + color("   ." + "=" * (panel_width - 8) + ".   ", SHADOW_CODE),
        left_pad + color("  /" + "=" * (panel_width - 4) + "\\  ", SHADOW_CODE),
    ]
    for idx in range(content_rows):
        text, code = full_content[idx] if idx < visible else (" " * inner, PARCHMENT_CODE)
        padded = pad_text_width(text, inner)
        lines.append(left_pad + color(" ||", SHADOW_CODE) + color(padded, code) + color("|| ", SHADOW_CODE))
    lines.append(left_pad + color("  \\" + "=" * (panel_width - 4) + "/  ", SHADOW_CODE))
    lines.append(left_pad + color("   '" + "=" * (panel_width - 8) + "'   ", SHADOW_CODE))
    return lines[:rows]


# Lässt die Schriftrolle kontrolliert ab- oder aufrollen, ohne den Prompt-Anker zu verlieren.
def animate_scroll(
    session: ReservedRenderSession,
    columns: int,
    title: str,
    subtitle: str,
    entries: list[str],
    footer: str = "",
    opening: bool = True,
) -> None:
    target_rows = max(3, min(SCROLL_PANEL_ROWS - 4, len(entries) + 3))
    sequence = range(1, target_rows + 1) if opening else range(target_rows, 0, -1)
    for reveal in sequence:
        current_columns = session.renderer.terminal_size().columns or columns
        session.render(build_scroll_panel_lines(current_columns, title, subtitle, entries, footer=footer, reveal_rows=reveal))
        time.sleep(SCROLL_FRAME_DELAY)


# Fragt eine Auswahl aus einer Liste ab und zeigt sie in einer ruhigen Schriftrollenansicht an.
def choose_from_list(
    session: ReservedRenderSession,
    cwd: Path,
    title: str,
    options: list[str],
    subtitle: str,
) -> str:
    while True:
        columns = session.renderer.terminal_size().columns
        entries = [f"{idx}. {option}" for idx, option in enumerate(options, start=1)]
        prompt = format_wizard_prompt(cwd, columns, "Auswahl 1-" + str(len(options)))
        raw = session.read(
            build_scroll_panel_lines(columns, title, subtitle, entries, footer="Waehle eine Zahl und bestaetige mit Enter."),
            prompt,
        ).strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        session.render(
            build_scroll_panel_lines(
                columns,
                title,
                subtitle,
                entries,
                footer="Ungueltige Auswahl. Bitte waehle eine gueltige Zahl.",
            ),
            "",
        )
        time.sleep(INTRO_FRAME_DELAY)


# Liest den Charakternamen ueber die Schriftrollenoberflaeche ein und begrenzt ihn auf 32 Zeichen.
def ask_name(session: ReservedRenderSession, cwd: Path) -> str:
    while True:
        columns = session.renderer.terminal_size().columns
        entries = [
            "Trage den Namen deines Charakters in die obere Zeile ein.",
            "Erlaubt sind 1 bis 32 sichtbare Zeichen.",
            "Die Schriftrolle bleibt waehrend der Eingabe oberhalb der Prompt-Zeile verankert.",
        ]
        raw = session.read(
            build_scroll_panel_lines(columns, "Namenssiegel", "Schriftrolle des Erwachens", entries, footer="Beispiel: Wuffie"),
            format_wizard_prompt(cwd, columns, "Name"),
        ).strip()
        if 1 <= len(raw) <= 32:
            return raw
        session.render(
            build_scroll_panel_lines(
                columns,
                "Namenssiegel",
                "Schriftrolle des Erwachens",
                entries,
                footer="Bitte gib einen Namen zwischen 1 und 32 Zeichen ein.",
            ),
            "",
        )
        time.sleep(INTRO_FRAME_DELAY)


# Fragt Attributpunkte ueber eine scrollartige Ruheansicht ab und verteilt sie schrittweise.
def allocate_attributes(session: ReservedRenderSession, cwd: Path, points: int = 12) -> dict[str, int]:
    base = {"strength": 10, "dexterity": 10, "accuracy": 10, "intelligence": 10, "wisdom": 10, "speed": 10}
    keys = list(base.keys())
    while points > 0:
        columns = session.renderer.terminal_size().columns
        entries = [f"Verbleibende Punkte: {points}", ""]
        for idx, key in enumerate(keys, start=1):
            entries.append(f"{idx}. {key:<13} {base[key]}")
        entries.append("")
        entries.append("Enter schliesst die Verteilung mit dem aktuellen Stand ab.")
        raw = session.read(
            build_scroll_panel_lines(
                columns,
                "Attributverteilung",
                "Die Pergamentrolle wartet ruhig auf jede einzelne Entscheidung",
                entries,
                footer="Waehle eine Zahl, um genau einen Punkt zu vergeben.",
            ),
            format_wizard_prompt(cwd, columns, "Attribut"),
        ).strip()
        if not raw:
            break
        if raw.isdigit() and 1 <= int(raw) <= len(keys):
            base[keys[int(raw) - 1]] += 1
            points -= 1
            continue
        session.render(
            build_scroll_panel_lines(
                columns,
                "Attributverteilung",
                "Die Pergamentrolle wartet ruhig auf jede einzelne Entscheidung",
                entries,
                footer="Ungueltige Auswahl. Bitte waehle eine Zahl aus der Liste.",
            ),
            "",
        )
        time.sleep(INTRO_FRAME_DELAY)
    return base


# Führt die Charaktererstellung lokal in einer gekapselten Schriftrolleninszenierung aus.
def run_character_creation(
    default_language: str = "de",
    renderer: ReservedTerminalRenderer | None = None,
    cwd: Path | None = None,
) -> dict[str, Any]:
    active_renderer = renderer or ReservedTerminalRenderer()
    active_cwd = cwd or Path.cwd()
    with ReservedRenderSession(active_renderer, SCROLL_PANEL_ROWS) as session:
        columns = session.renderer.terminal_size().columns
        animate_scroll(
            session,
            columns,
            "Schriftrolle der Herkunft",
            "Die Pergamentkanten rollen sich langsam aus.",
            [
                "Name, Herkunft, Gestalt und Kampfklasse werden nacheinander besiegelt.",
                "Die Eingabezeile bleibt dabei stets die letzte Zeile des Terminals.",
                "Erst nach Abschluss zieht sich die Rolle wieder sauber zusammen.",
            ],
            footer="Die Schriftrolle ist bereit.",
            opening=True,
        )
        name = ask_name(session, active_cwd)
        faction = choose_from_list(session, active_cwd, "Fraktionssiegel", CHARACTER_FACTIONS, "Waehle die politische Herkunft deines Charakters.")
        race = choose_from_list(session, active_cwd, "Rassenkunde", CHARACTER_RACES, "Waehle die leibliche Gestalt, in der du erwachst.")
        clazz = choose_from_list(session, active_cwd, "Kampfklasse", CHARACTER_CLASSES, "Waehle die Disziplin, die dein Auftreten praegen wird.")
        attrs = allocate_attributes(session, active_cwd, 12)
        summary_columns = session.renderer.terminal_size().columns
        summary_entries = [
            f"Name: {name}",
            f"Fraktion: {faction}",
            f"Rasse: {race}",
            f"Klasse: {clazz}",
            "",
            *[f"{key:<13} {value}" for key, value in attrs.items()],
        ]
        session.read(
            build_scroll_panel_lines(
                summary_columns,
                "Siegel abgeschlossen",
                "Die Schriftrolle zeigt noch einmal den finalen Charakterzustand",
                summary_entries,
                footer="Mit Enter wird die Rolle versiegelt und wieder eingerollt.",
            ),
            format_wizard_prompt(active_cwd, summary_columns, "Enter zum Abschliessen"),
        )
        animate_scroll(
            session,
            summary_columns,
            "Siegel abgeschlossen",
            "Die Pergamentrolle zieht sich geordnet zurueck.",
            summary_entries,
            footer="Uebergang in den Live-Betrieb",
            opening=False,
        )
    return {
        "character_name": name,
        "faction": faction,
        "race_name": race,
        "class_name": clazz,
        "attributes": attrs,
        "language": default_language,
    }


def is_character_command(raw: str) -> bool:
    if not raw:
        return False
    return raw.strip().split()[0].lower() in CHARACTER_COMMAND_ALIASES


# Erkennt lokale Steuerungsbefehle fuer das explizite Controller-/Observer-Modell.
def is_control_command(raw: str) -> bool:
    if not raw:
        return False
    return raw.strip().split()[0].lower() in CONTROL_COMMAND_ALIASES


# Erkennt lokale Matrix-/Peer-Diagnosebefehle fuer denselben serverseitigen Public-Contract wie WWW.
def is_matrix_command(raw: str) -> bool:
    if not raw:
        return False
    return raw.strip().split()[0].lower() in MATRIX_COMMAND_ALIASES


# Normalisiert einen eingegebenen Befehl fuer lokale Alias- und Sicherheitspruefungen.
def normalize_command_query(text: str) -> str:
    return " ".join((text or "").strip().lower().replace("_", " ").split())


# Findet den passendsten serverseitigen Command-Eintrag aus dem letzten Snapshot fuer einen lokalen Querystring.
def find_command_detail(snapshot: dict[str, Any] | None, raw: str) -> dict[str, Any] | None:
    if not snapshot:
        return None
    details = list(snapshot.get("command_details", []))
    normalized = normalize_command_query(raw)
    if not normalized:
        return None
    best: tuple[int, dict[str, Any]] | None = None
    for entry in details:
        aliases = list(entry.get("aliases", [])) or [entry.get("usage", "")]
        for alias in aliases:
            normalized_alias = normalize_command_query(alias)
            if not normalized_alias:
                continue
            if normalized == normalized_alias or normalized.startswith(normalized_alias + " "):
                score = len(normalized_alias)
                if best is None or score > best[0]:
                    best = (score, entry)
    return best[1] if best else None


# Prueft lokal, ob ein Spielkommando fuer Beobachter rein lesend und damit weiterhin erlaubt ist.
def is_observer_safe_game_command(snapshot: dict[str, Any] | None, raw: str) -> bool:
    normalized = normalize_command_query(raw)
    if not normalized:
        return True
    if normalized == "help" or normalized.startswith("help "):
        return True
    detail = find_command_detail(snapshot, raw)
    if detail is not None and bool(detail.get("observer_safe")):
        return True
    for pattern in OBSERVER_SAFE_COMMAND_PATTERNS:
        if normalized == pattern or normalized.startswith(pattern + " "):
            return True
    return False


# Ermittelt, ob diese Sitzung laut letztem Snapshot aktuell schreibend auf denselben Charakterzustand zugreifen darf.
def control_write_allowed(snapshot: dict[str, Any] | None) -> bool:
    if not snapshot:
        return True
    status = dict(snapshot.get("status", {}))
    if not status.get("control_mode"):
        return True
    return bool(status.get("control_write_allowed", False))


# Gibt fuer Beobachter eine einheitliche lokale Sperrmeldung aus, bevor ein Schreibpfad an den Server geht.
def guard_observer_write(snapshot: dict[str, Any] | None, label: str) -> bool:
    if control_write_allowed(snapshot):
        return False
    print(f"'{label}' ist fuer diese Sitzung aktuell read-only.")
    if snapshot is not None:
        print(format_control_status(snapshot))
    print("Nutze 'control take', um diese Sitzung vor schreibenden Aktionen explizit zur aktiven Steuerung zu machen.")
    return True


# Zeigt die lokale Befehlsstruktur fuer die serverseitige Charakterverwaltung an.
def character_command_tree() -> str:
    return "\n".join(
        [
            color("=== Character Command Tree ===", "36"),
            "character help",
            "  Zeigt diese Befehlsübersicht an.",
            "character list",
            "  Listet alle Charaktere des aktuellen Accounts auf.",
            "character new",
            "  Startet die lokale Charaktererstellung und aktiviert den neuen Charakter sofort.",
            "character use <index|character_id|name>",
            "  Wechselt den aktiven Charakter für denselben serverseitigen Account.",
        ]
    )


def character_command_help(topic: str = "") -> str:
    normalized = topic.strip().lower()
    help_map = {
        "list": "character list\nZeigt alle serverseitig bekannten Charaktere deines aktuellen Accounts an. Markiert wird auch, welcher Charakter gerade aktiv ist und damit sowohl im Terminal als auch im WWW denselben Zustand liefert.",
        "new": "character new\nStartet die lokale Charaktererstellung im Terminal. Nach erfolgreicher Erstellung wird der neue Charakter sofort auf dem ShellRPG-server aktiviert und beide Interfaces sehen denselben neuen Zustand.",
        "create": "character new\nStartet die lokale Charaktererstellung im Terminal. Nach erfolgreicher Erstellung wird der neue Charakter sofort auf dem ShellRPG-server aktiviert und beide Interfaces sehen denselben neuen Zustand.",
        "use": "character use <index|character_id|name>\nWechselt den aktiven Charakter innerhalb desselben Accounts. Du kannst dafuer entweder die Listenposition, die character_id oder den exakten Namen aus der Charakterliste verwenden.",
        "select": "character use <index|character_id|name>\nWechselt den aktiven Charakter innerhalb desselben Accounts. Du kannst dafuer entweder die Listenposition, die character_id oder den exakten Namen aus der Charakterliste verwenden.",
        "switch": "character use <index|character_id|name>\nWechselt den aktiven Charakter innerhalb desselben Accounts. Du kannst dafuer entweder die Listenposition, die character_id oder den exakten Namen aus der Charakterliste verwenden.",
    }
    if not normalized:
        return character_command_tree()
    return help_map.get(normalized, character_command_tree())


def sync_profile_identity(
    profile: dict[str, Any],
    api: ApiClient,
    snapshot: dict[str, Any] | None = None,
    selected_entry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    updated = dict(profile)
    updated["character_name"] = api.character_name
    updated["player_account_id"] = api.player_account_id
    updated["device_id"] = api.device_id
    if selected_entry:
        for key in ["faction", "race_name", "class_name"]:
            value = selected_entry.get(key)
            if value:
                updated[key] = value
    if snapshot:
        status = dict(snapshot.get("status", {}))
        for key in ["character_name", "race_name", "class_name", "language"]:
            value = status.get(key)
            if value:
                updated[key] = value
    return updated


def format_character_overview(overview: dict[str, Any]) -> str:
    if not overview.get("ok"):
        return overview.get("message", "Charakterliste konnte nicht geladen werden.")
    entries = list(overview.get("entries", []))
    header = [
        color("=== Charaktere ===", "36"),
        f"Account: {overview.get('player_account_id', 'unbekannt')}",
    ]
    if not entries:
        header.append("Noch keine Charaktere im Account vorhanden.")
        return "\n".join(header)
    for idx, entry in enumerate(entries, start=1):
        marker = "*" if entry.get("active") else "-"
        header.append(
            f"{marker} {idx}. {entry.get('character_name', '?')} [{entry.get('character_id', '?')}] "
            f"· {entry.get('class_name', '?')}/{entry.get('race_name', '?')} "
            f"· {entry.get('faction', '?')} · Lvl {entry.get('level', '?')} · {entry.get('coords_label', '?')}"
        )
    return "\n".join(header)


def resolve_character_selection(selector: str, entries: list[dict[str, Any]]) -> dict[str, Any] | None:
    token = selector.strip()
    if not token:
        return None
    if token.isdigit():
        index = int(token)
        if 1 <= index <= len(entries):
            return entries[index - 1]
    for entry in entries:
        if entry.get("character_id") == token:
            return entry
    lowered = token.casefold()
    for entry in entries:
        if str(entry.get("character_name", "")).casefold() == lowered:
            return entry
    return None


def handle_character_command(
    raw: str,
    api: ApiClient,
    profile: dict[str, Any],
    current_snapshot: dict[str, Any] | None = None,
    renderer: ReservedTerminalRenderer | None = None,
    cwd: Path | None = None,
) -> tuple[bool, dict[str, Any], dict[str, Any] | None]:
    if not is_character_command(raw):
        return False, profile, None
    current_profile = dict(profile)
    parts = raw.strip().split(maxsplit=2)
    action = parts[1].lower() if len(parts) > 1 else "help"
    if len(parts) > 2 and parts[2].strip().lower() in {"help", "--help", "-h", "?"}:
        print(character_command_help(action))
        return True, sync_profile_identity(current_profile, api), None
    if action in {"help", "tree"}:
        topic = parts[2].strip() if len(parts) > 2 else ""
        print(character_command_help(topic))
        try:
            print(format_character_overview(api.list_characters()))
        except Exception as exc:
            print(f"Charakterliste nicht verfügbar: {exc}")
        return True, sync_profile_identity(current_profile, api), None
    if action in {"list", "ls"}:
        try:
            print(format_character_overview(api.list_characters()))
        except Exception as exc:
            print(f"Charakterliste nicht verfügbar: {exc}")
        return True, sync_profile_identity(current_profile, api), None
    if action in {"new", "create"}:
        live_snapshot = current_snapshot or api.state()
        if guard_observer_write(live_snapshot, "character new"):
            return True, sync_profile_identity(current_profile, api, snapshot=live_snapshot), live_snapshot
        payload = run_character_creation(
            str(current_profile.get("language", "de") or "de"),
            renderer=renderer,
            cwd=cwd,
        )
        try:
            result = api.create_character(payload)
            if not result.get("ok"):
                print(result.get("message", "Charaktererstellung fehlgeschlagen."))
                return True, sync_profile_identity(current_profile, api), None
            snapshot = api.state()
        except Exception as exc:
            print(f"Charaktererstellung fehlgeschlagen: {exc}")
            return True, sync_profile_identity(current_profile, api), None
        current_profile.update(payload)
        current_profile = sync_profile_identity(current_profile, api, snapshot=snapshot)
        print(
            result.get(
                "message",
                f"Charakter {result.get('character_name', api.character_name)} wurde erstellt und aktiviert.",
            )
        )
        try:
            print(format_character_overview(api.list_characters()))
        except Exception:
            pass
        return True, current_profile, snapshot
    if action in {"use", "select", "switch"}:
        if len(parts) < 3:
            print("Bitte gib einen Index, eine character_id oder einen Namen an.")
            print(character_command_tree())
            return True, sync_profile_identity(current_profile, api), None
        live_snapshot = current_snapshot or api.state()
        if guard_observer_write(live_snapshot, "character use"):
            return True, sync_profile_identity(current_profile, api, snapshot=live_snapshot), live_snapshot
        try:
            overview = api.list_characters()
        except Exception as exc:
            print(f"Charakterliste nicht verfügbar: {exc}")
            return True, sync_profile_identity(current_profile, api), None
        entry = resolve_character_selection(parts[2], list(overview.get("entries", [])))
        if entry is None:
            print("Charakterauswahl nicht gefunden.")
            print(format_character_overview(overview))
            return True, sync_profile_identity(current_profile, api), None
        try:
            result = api.select_character(str(entry.get("character_id", "")))
            snapshot = api.state()
        except Exception as exc:
            print(f"Charakterwechsel fehlgeschlagen: {exc}")
            return True, sync_profile_identity(current_profile, api), None
        current_profile = sync_profile_identity(current_profile, api, snapshot=snapshot, selected_entry=entry)
        print(result.get("message", f"Aktiver Charakter ist jetzt {api.character_name}."))
        try:
            print(format_character_overview(api.list_characters()))
        except Exception:
            pass
        return True, current_profile, snapshot
    print(f"Unbekannter character-Unterbefehl: {action}")
    print(character_command_tree())
    return True, sync_profile_identity(current_profile, api), None


# Uebersetzt die serverseitige Rollenkennung in eine lesbare Terminalbeschreibung.
def describe_control_role(status: dict[str, Any]) -> str:
    role = str(status.get("control_role", "") or "")
    if role == "active-controller":
        return "aktive Steuerung"
    if role == "observer":
        return "Beobachter"
    return role or "unbekannt"


# Baut eine kompakte Statusansicht fuer das explizite Controller-/Observer-Modell.
def format_control_status(snapshot: dict[str, Any]) -> str:
    status = dict(snapshot.get("status", {}))
    lines = [
        color("=== Steuerungsrolle ===", "36"),
        f"Rolle: {describe_control_role(status)}",
        f"Status: {status.get('control_state', 'free')}",
        f"Modell: {status.get('control_mode', 'controller-observer')}",
        f"Lease: {int(status.get('control_lease_seconds_left', 0))}s",
    ]
    holder = str(status.get("control_holder_label", "") or "")
    action = str(status.get("control_action", "") or "")
    if holder:
        lines.append(f"Aktueller Halter: {holder}")
    if action:
        lines.append(f"Letzte Steuerungsaktion: {action}")
    lines.append(f"Takeover moeglich: {'ja' if status.get('control_takeover_available') else 'nein'}")
    lines.append(f"Freigabe moeglich: {'ja' if status.get('control_can_release') else 'nein'}")
    return "\n".join(lines)


# Zeigt die lokalen Terminalbefehle fuer das explizite Steuerungsmodell an.
def control_command_tree() -> str:
    return "\n".join(
        [
            color("=== Control Command Tree ===", "36"),
            "control help",
            "  Zeigt diese Steuerungsuebersicht an.",
            "control status",
            "  Zeigt, ob diese Sitzung aktive Steuerung oder Beobachter ist.",
            "control take",
            "  Uebernimmt die aktive Steuerung explizit fuer diese Sitzung.",
            "control release",
            "  Gibt die aktive Steuerung dieser Sitzung wieder frei.",
        ]
    )


# Liefert die ausfuehrliche Hilfe zu den lokalen Steuerungsbefehlen des Clients.
def control_command_help(topic: str = "") -> str:
    normalized = topic.strip().lower()
    help_map = {
        "status": (
            "control status\n"
            "Liest den aktuellen serverseitigen Rollenstatus. Eine Sitzung ist entweder aktive Steuerung oder Beobachter."
        ),
        "take": (
            "control take\n"
            "Fordert die aktive Steuerung explizit fuer diese Terminal-Sitzung an. Andere Sitzungen werden dadurch zu Beobachtern."
        ),
        "takeover": (
            "control take\n"
            "Fordert die aktive Steuerung explizit fuer diese Terminal-Sitzung an. Andere Sitzungen werden dadurch zu Beobachtern."
        ),
        "release": (
            "control release\n"
            "Gibt die aktive Steuerung frei, damit das WWW oder eine andere Sitzung kontrolliert uebernehmen kann."
        ),
    }
    if not normalized:
        return control_command_tree()
    return help_map.get(normalized, control_command_tree())


# Behandelt die lokalen Steuerungsbefehle fuer aktives Uebernehmen oder Beobachten desselben Serverzustands.
def handle_control_command(raw: str, api: ApiClient) -> tuple[bool, dict[str, Any] | None]:
    if not is_control_command(raw):
        return False, None
    parts = raw.strip().split(maxsplit=2)
    action = parts[1].lower() if len(parts) > 1 else "help"
    if len(parts) > 2 and parts[2].strip().lower() in {"help", "--help", "-h", "?"}:
        print(control_command_help(action))
        return True, None
    if action in {"help", "tree"}:
        print(control_command_help(parts[2].strip() if len(parts) > 2 else ""))
        return True, None
    if action in {"status", "show"}:
        snapshot = api.state()
        print(format_control_status(snapshot))
        return True, snapshot
    if action in {"take", "takeover"}:
        result = api.take_control()
        print(result.get("message", "Steuerung uebernommen."))
        snapshot = api.state()
        print(format_control_status(snapshot))
        return True, snapshot
    if action in {"release", "free"}:
        result = api.release_control()
        print(result.get("message", "Steuerung freigegeben."))
        snapshot = api.state()
        print(format_control_status(snapshot))
        return True, snapshot
    print(f"Unbekannter control-Unterbefehl: {action}")
    print(control_command_tree())
    return True, None


def normalize_matrix_count_map(values: Any) -> dict[str, int]:
    if not isinstance(values, dict):
        return {}
    normalized: dict[str, int] = {}
    for key, raw_value in values.items():
        label = str(key or "").strip()
        if not label:
            continue
        try:
            amount = int(raw_value or 0)
        except (TypeError, ValueError):
            continue
        if amount <= 0:
            continue
        normalized[label] = normalized.get(label, 0) + amount
    return dict(sorted(normalized.items(), key=lambda item: (-item[1], item[0])))


def format_matrix_timestamp(value: Any) -> str:
    if isinstance(value, (int, float)):
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            numeric = 0.0
        if numeric <= 0:
            return "-"
        try:
            return datetime.fromtimestamp(numeric).strftime("%Y-%m-%d %H:%M:%S")
        except (OverflowError, OSError, ValueError):
            return str(value)
    text = str(value or "").strip()
    if not text:
        return "-"
    if text.endswith("Z"):
        text = text[:-1] + " UTC"
    return text.replace("T", " ")


def format_matrix_count_line(label: str, values: Any, limit: int = 4) -> str:
    counts = list(normalize_matrix_count_map(values).items())
    if not counts:
        return f"{label}: -"
    visible = ", ".join(f"{name}={amount}" for name, amount in counts[:limit])
    hidden = len(counts) - limit
    if hidden > 0:
        visible += f", +{hidden} weitere"
    return f"{label}: {visible}"


def matrix_preview_text(value: Any, limit: int = 4) -> str:
    payload = dict(value or {})
    preview = [str(entry) for entry in list(payload.get("preview", [])) if str(entry)]
    if not preview:
        count = int(payload.get("count", 0) or 0)
        return "-" if count <= 0 else f"{count} Eintraege"
    visible = ", ".join(preview[:limit])
    count = int(payload.get("count", len(preview)) or len(preview))
    hidden = max(0, count - min(len(preview), limit))
    if hidden > 0 or bool(payload.get("truncated")):
        visible += f", +{max(hidden, 1)} weitere"
    return visible


def normalize_matrix_search_terms(raw: str) -> list[str]:
    return [part.strip().lower() for part in str(raw or "").split() if part.strip()]


def matrix_conflict_search_text(conflict: dict[str, Any]) -> str:
    parts: list[str] = [
        str(conflict.get("character_name", "") or ""),
        str(conflict.get("conflict_id", "") or ""),
        str(conflict.get("max_severity", "") or ""),
        str(conflict.get("max_tier", "") or ""),
    ]
    for group in list(conflict.get("merged_field_groups", [])):
        parts.append(str(dict(group or {}).get("group", "") or ""))
    parts.extend(normalize_matrix_count_map(conflict.get("severity_counts")).keys())
    parts.extend(normalize_matrix_count_map(conflict.get("reason_code_counts")).keys())
    for comparison in list(conflict.get("field_comparisons", [])):
        current = dict(comparison or {})
        parts.extend(
            [
                str(current.get("field", "") or ""),
                str(current.get("field_conflict_id", "") or ""),
                str(current.get("group", "") or ""),
                str(current.get("merge_mode", "") or ""),
                str(current.get("winner_side", "") or ""),
                str(current.get("max_severity", "") or ""),
                str(current.get("max_tier", "") or ""),
            ]
        )
        parts.extend(normalize_matrix_count_map(current.get("severity_counts")).keys())
        parts.extend(normalize_matrix_count_map(current.get("reason_code_counts")).keys())
        delta_summary = dict(current.get("delta_summary", {}))
        parts.extend(normalize_matrix_count_map(delta_summary.get("hidden_priority_reason_code_counts")).keys())
        for key in ("added_preview", "changed_preview"):
            parts.extend(str(entry) for entry in list(delta_summary.get(key, [])) if str(entry))
        for entry in list(delta_summary.get("priority_preview", [])):
            preview = dict(entry or {})
            parts.extend(
                [
                    str(preview.get("delta_kind", "") or ""),
                    str(preview.get("label", "") or ""),
                    str(preview.get("reason_code", "") or ""),
                    str(preview.get("reason", "") or ""),
                    str(preview.get("severity", "") or ""),
                    str(preview.get("tier", "") or ""),
                ]
            )
    return " ".join(part.lower() for part in parts if part)


def filter_matrix_conflicts(snapshot: dict[str, Any], query: str = "") -> list[dict[str, Any]]:
    conflicts = list(snapshot.get("character_conflicts", []))
    terms = normalize_matrix_search_terms(query)
    if not terms:
        return conflicts
    return [
        conflict
        for conflict in conflicts
        if all(term in matrix_conflict_search_text(dict(conflict or {})) for term in terms)
    ]


def format_matrix_priority_entry(entry: Any) -> str:
    payload = dict(entry or {})
    kind_map = {"plus": "Plus", "upgrade": "Upgrade"}
    kind = kind_map.get(str(payload.get("delta_kind", "") or "").lower(), "Delta")
    severity = str(payload.get("severity", "-") or "-")
    tier = int(payload.get("tier", 0) or 0)
    weight = int(payload.get("weight", 0) or 0)
    return (
        f"{kind} {payload.get('label', '?')} · {severity}/Tier {tier or '-'} · "
        f"{payload.get('reason_code', '?')} · {payload.get('reason', '-')} · W{weight}"
    )


def format_matrix_hotspots(hotspots: Any) -> str:
    payload = dict(hotspots or {})
    top_characters = list(payload.get("top_characters", []))
    reason_codes = list(payload.get("reason_codes", []))
    peers = list(payload.get("peers", []))
    lines = [color("=== Matrix-Hotspots ===", "36")]
    if not top_characters and not reason_codes and not peers:
        lines.append("Keine Hotspots gemeldet.")
        return "\n".join(lines)
    if top_characters:
        rendered = ", ".join(
            f"{entry.get('character_name', '?')} ({entry.get('max_severity', '-')})"
            for entry in top_characters[:3]
        )
        lines.append(f"Charaktere: {rendered}")
    if reason_codes:
        rendered = ", ".join(
            f"{entry.get('reason_code', '?')}={int(entry.get('count', 0) or 0)}"
            for entry in reason_codes[:4]
        )
        lines.append(f"Gruppen: {rendered}")
    if peers:
        rendered = ", ".join(
            f"{entry.get('server_id', '?')} ({entry.get('relation', '?')})"
            for entry in peers[:3]
        )
        lines.append(f"Peers: {rendered}")
    return "\n".join(lines)


def format_matrix_peer_report(snapshot: dict[str, Any], limit: int = 8) -> str:
    local = dict(snapshot.get("local", {}))
    chosen = dict(snapshot.get("chosen", {}))
    peers = list(snapshot.get("peers", []))
    lines = [color("=== Matrix-Peers ===", "36")]
    lines.append(
        f"Lokal: {local.get('server_id', '?')} · Tick {int(local.get('latest_tick', 0) or 0)} · "
        f"Savepoint {format_matrix_timestamp(local.get('latest_savepoint_ts', 0.0))}"
    )
    chosen_source = str(chosen.get("source", "local") or "local")
    lines.append(
        f"Bevorzugter Stand: {chosen.get('server_id', local.get('server_id', '?'))} "
        f"via {chosen_source} · Tick {int(chosen.get('latest_tick', 0) or 0)}"
    )
    if not peers:
        lines.append("Keine Peer-Diagnostik vorhanden.")
        return "\n".join(lines)
    for entry in peers[:limit]:
        try:
            tick_diff = int(entry.get("tick_diff", 0) or 0)
        except (TypeError, ValueError):
            tick_diff = 0
        label_parts = [
            str(entry.get("server_id", "?") or "?"),
            "frisch" if bool(entry.get("fresh")) else "stale",
            str(entry.get("relation", "?") or "?"),
        ]
        if tick_diff:
            label_parts.append(f"Tickdiff {tick_diff:+d}")
        if bool(entry.get("preferred")):
            label_parts.append("bevorzugt")
        source = str(entry.get("source", "") or "")
        if source:
            label_parts.append(source)
        lines.append("- " + " · ".join(label_parts))
    hidden = len(peers) - limit
    if hidden > 0:
        lines.append(f"... {hidden} weitere Peers ausgeblendet.")
    return "\n".join(lines)


def format_matrix_conflict_report(
    snapshot: dict[str, Any],
    limit: int = 5,
    field_limit: int = 3,
    query: str = "",
) -> str:
    summary = dict(snapshot.get("conflict_summary", {}))
    conflicts = filter_matrix_conflicts(snapshot, query=query)
    lines = [color("=== Matrix-Konflikte ===", "36")]
    if query.strip():
        lines.append(f"Filter: {query.strip()}")
    lines.append(
        f"Charakterkonflikte: {len(conflicts)}/{int(summary.get('character_conflict_count', len(conflicts)) or 0)} Treffer · "
        f"Kritisch: {int(summary.get('critical_character_conflict_count', 0) or 0)} · "
        f"Feld-Merges: {int(summary.get('field_merge_count', 0) or 0)}"
    )
    if not conflicts:
        lines.append("Keine Character-Konflikte fuer diesen Filter gemeldet.")
        return "\n".join(lines)
    for conflict in conflicts[:limit]:
        history = dict(conflict.get("history", {}))
        merged_groups = ", ".join(
            str(dict(group or {}).get("group", "?") or "?")
            for group in list(conflict.get("merged_field_groups", []))
            if str(dict(group or {}).get("group", "") or "")
        )
        lines.append(
            "- "
            + f"{conflict.get('character_name', '?')} "
            + f"[{conflict.get('conflict_id', '?')}] "
            + f"· {conflict.get('max_severity', '-')}/Tier {int(conflict.get('max_tier', 0) or 0)} "
            + f"· {int(conflict.get('field_comparison_count', len(conflict.get('field_comparisons', []))) or 0)} Feldvergleiche "
            + f"· gesehen {int(history.get('seen_count', 0) or 0)} "
            + f"· offen {'ja' if history.get('still_open') else 'nein'}"
        )
        if merged_groups:
            lines.append(f"    Gruppen: {merged_groups}")
        comparisons = list(conflict.get("field_comparisons", []))
        for comparison in comparisons[:field_limit]:
            delta_summary = dict(comparison.get("delta_summary", {}))
            priority_preview = list(delta_summary.get("priority_preview", []))
            preview = ", ".join(
                f"{entry.get('label', '?')} ({entry.get('reason_code', '?')})"
                for entry in priority_preview[:2]
            ) or "-"
            lines.append(
                "  * "
                + f"{comparison.get('field', '?')} [{comparison.get('field_conflict_id', '?')}] "
                + f"· {comparison.get('max_severity', '-')}/Tier {int(comparison.get('max_tier', 0) or 0)} "
                + f"· {preview}"
            )
            hidden_reason_codes = normalize_matrix_count_map(delta_summary.get("hidden_priority_reason_code_counts"))
            if hidden_reason_codes:
                lines.append("    " + format_matrix_count_line("Verdeckt", hidden_reason_codes, limit=3))
        hidden_fields = len(comparisons) - field_limit
        if hidden_fields > 0:
            lines.append(f"    ... {hidden_fields} weitere Feldvergleiche ausgeblendet.")
    hidden_conflicts = len(conflicts) - limit
    if hidden_conflicts > 0:
        lines.append(f"... {hidden_conflicts} weitere Character-Konflikte ausgeblendet.")
    return "\n".join(lines)


def format_matrix_conflict_detail(snapshot: dict[str, Any], query: str, field_limit: int = 6) -> str:
    lines = [color("=== Matrix-Konflikt-Drilldown ===", "36")]
    normalized_query = query.strip()
    if not normalized_query:
        lines.append("Nutzung: matrix inspect <conflict_id|field_conflict_id|character|filter>")
        return "\n".join(lines)
    conflicts = filter_matrix_conflicts(snapshot, query=normalized_query)
    if not conflicts:
        lines.append(f"Keine Konflikte fuer '{normalized_query}' gefunden.")
        return "\n".join(lines)
    lines.append(f"Query: {normalized_query}")
    lines.append(f"Treffer: {len(conflicts)}")
    for conflict in conflicts[:3]:
        history = dict(conflict.get("history", {}))
        lines.append("")
        lines.append(
            f"{conflict.get('character_name', '?')} [{conflict.get('conflict_id', '?')}] "
            + f"· {conflict.get('max_severity', '-')}/Tier {int(conflict.get('max_tier', 0) or 0)} "
            + f"· offen {'ja' if history.get('still_open') else 'nein'} "
            + f"· gesehen {int(history.get('seen_count', 0) or 0)}"
        )
        merged_groups = ", ".join(
            str(dict(group or {}).get("group", "?") or "?")
            for group in list(conflict.get("merged_field_groups", []))
            if str(dict(group or {}).get("group", "") or "")
        )
        if merged_groups:
            lines.append(f"Gruppen: {merged_groups}")
        lines.append(format_matrix_count_line("Severity", conflict.get("severity_counts")))
        lines.append(format_matrix_count_line("Reason-Codes", conflict.get("reason_code_counts")))
        comparisons = list(conflict.get("field_comparisons", []))
        query_lower = normalized_query.lower()
        exact_field_matches = [
            comparison
            for comparison in comparisons
            if str(dict(comparison or {}).get("field_conflict_id", "") or "").lower() == query_lower
        ]
        shown = exact_field_matches or comparisons[:field_limit]
        for comparison in shown:
            current = dict(comparison or {})
            delta_summary = dict(current.get("delta_summary", {}))
            lines.append(
                "  * "
                + f"{current.get('field', '?')} [{current.get('field_conflict_id', '?')}] "
                + f"· {current.get('max_severity', '-')}/Tier {int(current.get('max_tier', 0) or 0)}"
            )
            lines.append(
                "    "
                + f"Gruppe: {current.get('group', '-') or '-'} · "
                + f"Merge: {current.get('merge_mode', '-') or '-'} · "
                + f"Gewinner: {current.get('winner_side', '-') or '-'}"
            )
            lines.append("    " + format_matrix_count_line("Severity", current.get("severity_counts"), limit=3))
            lines.append("    " + format_matrix_count_line("Reason-Codes", current.get("reason_code_counts"), limit=3))
            lines.append("    " + f"Preferred: {matrix_preview_text(current.get('preferred'))}")
            lines.append("    " + f"Fallback: {matrix_preview_text(current.get('fallback'))}")
            lines.append("    " + f"Gemerged: {matrix_preview_text(current.get('merged'))}")
            lines.append(
                "    "
                + f"Delta: total {int(delta_summary.get('delta_count', 0) or 0)} · "
                + f"neu {int(delta_summary.get('added_count', 0) or 0)} · "
                + f"upgrades {int(delta_summary.get('changed_count', 0) or 0)}"
            )
            added_preview = list(delta_summary.get("added_preview", []))
            changed_preview = list(delta_summary.get("changed_preview", []))
            if added_preview:
                lines.append("    " + f"Neu: {', '.join(str(entry) for entry in added_preview[:4])}")
            if changed_preview:
                lines.append("    " + f"Upgrades: {', '.join(str(entry) for entry in changed_preview[:4])}")
            priority_preview = list(delta_summary.get("priority_preview", []))
            if priority_preview:
                lines.append("    Priorisiert:")
                for entry in priority_preview[:4]:
                    lines.append("      - " + format_matrix_priority_entry(entry))
            hidden_reason_codes = normalize_matrix_count_map(delta_summary.get("hidden_priority_reason_code_counts"))
            if hidden_reason_codes:
                lines.append("    " + format_matrix_count_line("Verdeckt", hidden_reason_codes, limit=3))
        hidden_fields = len(comparisons) - len(shown)
        if hidden_fields > 0 and not exact_field_matches:
            lines.append(f"    ... {hidden_fields} weitere Feldvergleiche fuer diesen Konflikt ausgeblendet.")
    hidden_conflicts = len(conflicts) - 3
    if hidden_conflicts > 0:
        lines.append("")
        lines.append(f"... {hidden_conflicts} weitere Konflikte fuer '{normalized_query}' ausgeblendet.")
    return "\n".join(lines)


def format_matrix_health_report(
    snapshot: dict[str, Any],
    *,
    include_hotspots: bool = False,
    include_peers: bool = False,
) -> str:
    health = dict(snapshot.get("health", {}))
    lines = [color("=== Servermatrix ===", "36")]
    lines.append(
        f"Status: {health.get('status', 'unknown')} · Grund: {health.get('reason', '-')} · "
        f"fresh/stale: {int(health.get('fresh_peer_count', 0) or 0)}/{int(health.get('stale_peer_count', 0) or 0)}"
    )
    lines.append(
        f"Letzter Sync: {health.get('last_sync_result', '-') or '-'} "
        + f"@ Tick {int(health.get('last_sync_tick', 0) or 0)} "
        + f"via {health.get('last_sync_source', '-') or '-'} "
        + f"({format_matrix_timestamp(health.get('last_sync_ts', 0.0))})"
    )
    max_tier = int(health.get("max_conflict_tier", 0) or 0)
    tier_text = f"Tier {max_tier}" if max_tier > 0 else "Tier -"
    lines.append(
        f"Konflikte: {int(health.get('character_conflict_count', 0) or 0)} Charaktere · "
        f"{int(health.get('field_merge_count', 0) or 0)} Feld-Merges · "
        f"{int(health.get('critical_character_conflict_count', 0) or 0)} kritisch"
    )
    lines.append(f"Maximale Schwere: {health.get('max_conflict_severity', '-') or '-'} · {tier_text}")
    lines.append(format_matrix_count_line("Severity", health.get("priority_severity_counts")))
    lines.append(format_matrix_count_line("Reason-Codes", health.get("priority_reason_code_counts")))
    if include_hotspots:
        lines.append("")
        lines.append(format_matrix_hotspots(snapshot.get("hotspots", {})))
    if include_peers:
        lines.append("")
        lines.append(format_matrix_peer_report(snapshot))
    return "\n".join(lines)


def compact_matrix_health_hint(snapshot: dict[str, Any] | None) -> str:
    if not isinstance(snapshot, dict):
        return "Mx: -"
    health = dict(snapshot.get("health", {}))
    raw_status = str(health.get("status", "") or "").strip().lower()
    if not raw_status:
        return "Mx: -"
    status_map = {
        "healthy": "ok",
        "degraded": "warn",
        "isolated": "solo",
        "syncing-needed": "sync",
        "disabled": "off",
        "unavailable": "na",
    }
    status = status_map.get(raw_status, raw_status[:6] or "?")
    try:
        peers = int(health.get("fresh_peer_count", 0) or 0)
    except (TypeError, ValueError):
        peers = 0
    try:
        conflicts = int(health.get("character_conflict_count", 0) or 0)
    except (TypeError, ValueError):
        conflicts = 0
    severity = str(health.get("max_conflict_severity", "") or "").strip().lower()
    if raw_status == "healthy":
        return f"Mx: {status}/{peers}p"
    details: list[str] = []
    if conflicts > 0:
        details.append(f"{conflicts}k")
    if severity:
        details.append(severity)
    if not details:
        reason = str(health.get("reason", "") or "").strip().lower()
        if reason:
            details.append(reason[:8])
    return f"Mx: {status}/{'/'.join(details[:2])}" if details else f"Mx: {status}"


def matrix_command_tree() -> str:
    return "\n".join(
        [
            color("=== Matrix Command Tree ===", "36"),
            "matrix help",
            "  Zeigt diese Matrix-/Peer-Diagnoseübersicht an.",
            "matrix health",
            "  Zeigt den kompakten Matrix-Gesundheitszustand mit Severity- und Reason-Code-Rollups.",
            "matrix status",
            "  Zeigt denselben Gesundheitszustand plus bevorzugten Peer-Stand und Peer-Liste.",
            "matrix conflicts [filter]",
            "  Zeigt Character-Konflikte mit Feld-Merges, IDs und Kurz-Diffs; optional gefiltert.",
            "matrix inspect <conflict_id|field_conflict_id|character>",
            "  Zeigt den Drilldown fuer einen Konflikt oder ein bestimmtes Feld.",
            "matrix hotspots",
            "  Zeigt auffällige Charaktere, Gruppen und Peers aus dem Hotspot-Rollup.",
            "matrix peers",
            "  Zeigt die ausführliche Peer-Diagnose ohne Konfliktfokus.",
        ]
    )


def matrix_command_help(topic: str = "") -> str:
    normalized = topic.strip().lower()
    help_map = {
        "health": (
            "matrix health\n"
            "Liest `/api/matrix/health` und zeigt den kompakten Matrixzustand "
            "inklusive Severity-/Reason-Code-Rollups und Hotspots."
        ),
        "status": (
            "matrix status\n"
            "Liest `/api/matrix/status` und zeigt dieselbe Matrixdiagnose "
            "zusätzlich mit Peer-Liste und bevorzugtem Stand."
        ),
        "conflicts": (
            "matrix conflicts [filter]\n"
            "Zeigt Character-Konflikte, stabile conflict_id-/field_conflict_id-Anker, "
            "Severity/Tier und kurze Priorisierungsdeltas. Ein optionaler Filter kann "
            "nach Charakter, Severity, Reason-Code, Feld oder Konflikt-ID suchen."
        ),
        "inspect": (
            "matrix inspect <conflict_id|field_conflict_id|character>\n"
            "Zeigt einen Drilldown fuer einen konkreten Character-Konflikt oder ein "
            "einzelnes Feld inklusive Preferred/Fallback/Gemerged-Preview und "
            "priorisierten Delta-Gruenden."
        ),
        "hotspots": (
            "matrix hotspots\n"
            "Zeigt nur die verdichteten Hotspots für Charaktere, Gruppen und Peers."
        ),
        "peers": (
            "matrix peers\n"
            "Zeigt die Peer-Diagnose aus `/api/matrix/status` mit Freshness, Relation, Tickdiff und Preferred-Hinweis."
        ),
    }
    if not normalized:
        return matrix_command_tree()
    return help_map.get(normalized, matrix_command_tree())


def handle_matrix_command(raw: str, api: ApiClient) -> bool:
    if not is_matrix_command(raw):
        return False
    parts = raw.strip().split(maxsplit=2)
    action = parts[1].lower() if len(parts) > 1 else "help"
    query = parts[2].strip() if len(parts) > 2 else ""
    if len(parts) > 2 and parts[2].strip().lower() in {"help", "--help", "-h", "?"}:
        print(matrix_command_help(action))
        return True
    if action in {"help", "tree"}:
        print(matrix_command_help(query))
        return True
    try:
        if action in {"health", "show", "summary"}:
            print(format_matrix_health_report(api.matrix_health(), include_hotspots=True))
            return True
        if action in {"status"}:
            print(format_matrix_health_report(api.matrix_status(), include_hotspots=True, include_peers=True))
            return True
        if action in {"conflicts"}:
            print(format_matrix_conflict_report(api.matrix_health(), query=query))
            return True
        if action in {"inspect", "conflict"}:
            print(format_matrix_conflict_detail(api.matrix_health(), query))
            return True
        if action in {"hotspots"}:
            print(format_matrix_hotspots(api.matrix_health().get("hotspots", {})))
            return True
        if action in {"peers"}:
            print(format_matrix_peer_report(api.matrix_status()))
            return True
    except Exception as exc:
        print(f"Matrixdiagnose nicht verfügbar: {exc}")
        print("Der private ShellRPG-server muss `/api/matrix/health` bzw. `/api/matrix/status` bereitstellen.")
        return True
    print(f"Unbekannter matrix-Unterbefehl: {action}")
    print(matrix_command_tree())
    return True


# Erkennt, ob der eingegebene Text als Spielkommando und nicht als normales Shell-Kommando behandelt werden soll.
def is_game_command(raw: str) -> bool:
    if not raw:
        return False
    first = raw.strip().split()[0].lower()
    return first in GAME_VERBS


# Führt Shell-Kommandos aus, behandelt Verzeichniswechsel lokal und kann Ausgaben bei Bedarf direkt an die echte Shell durchreichen.
def run_shell_command(raw: str, cwd: Path, capture_output: bool = True) -> tuple[Path, str]:
    stripped = raw.strip()
    if stripped.lower() in {"pwd", "cd"}:
        return cwd, str(cwd)
    if stripped.lower().startswith("cd "):
        target = stripped[3:].strip().strip('"')
        nxt = (cwd / target).resolve() if not Path(target).is_absolute() else Path(target).resolve()
        if nxt.exists() and nxt.is_dir():
            return nxt, str(nxt)
        return cwd, f"Pfad nicht gefunden: {target}"
    try:
        run_kwargs: dict[str, Any] = {"shell": True, "cwd": str(cwd), "text": True}
        if capture_output:
            run_kwargs["capture_output"] = True
        result = subprocess.run(stripped, **run_kwargs)
        if capture_output:
            output = (result.stdout or "") + (result.stderr or "")
            return cwd, output.strip() or f"Rückgabecode: {result.returncode}"
        return cwd, ""
    except Exception as exc:
        return cwd, f"Shell-Kommando fehlgeschlagen: {exc}"


# Ordnet die Mondbeschriftung einer kleinen ASCII-Phasenskala zu.
def moon_scale(label: str) -> str:
    phases = ["Neumond", "Zunehmende Sichel", "Erstes Viertel", "Zunehmender Mond", "Vollmond", "Abnehmender Mond", "Letztes Viertel", "Abnehmende Sichel"]
    glyphs = ["○", "◔", "◑", "◕", "●", "◕", "◑", "◔"]
    for idx, name in enumerate(phases):
        if name.lower() in label.lower():
            return glyphs[idx]
    return "◔"


# Ordnet die Venusbeschriftung einer kleinen ASCII-Skala zu.
def venus_scale(label: str) -> str:
    mapping = {"Morgen": "◔", "Tag": "◑", "Dämmerung": "◕", "Nacht": "○"}
    for key, glyph in mapping.items():
        if key.lower() in label.lower():
            return glyph
    return "◑"


# Erzeugt die vier kompakten Statuszeilen und kuerzt sie strikt auf genau eine physische Terminalzeile ein.
def compact_status_lines(
    snapshot: dict,
    spinner_index: int,
    columns: int | None = None,
    matrix_snapshot: dict[str, Any] | None = None,
) -> list[str]:
    width = columns or shutil.get_terminal_size((100, 30)).columns
    status = snapshot["status"]
    action = status.get("active_action", "idle")
    overlay = status.get("overlay_message", "") or f"Aktiv: {action}"
    location = status.get("location_label", "?")
    if action in {"idle", ""}:
        live = f"Dein Ritter macht gerade nichts ... {SPINNERS[spinner_index % len(SPINNERS)]} [{location}]"
    else:
        live = f"{overlay} {SPINNERS[spinner_index % len(SPINNERS)]}"
    lines = [
        live,
        f"[ {status['character_name']} | {status['class_name']}/{status['race_name']} | Lvl {status['level']} | {location} [{status['coords_label']}] | HP {status['hp_current']}/{status['hp_max']} | MP {status['mana_current']}/{status['mana_max']} ]",
        f"[ {status['gold']} Gold / {status['silver']} Silber | Hunger: {status['hunger']} | Wetter: {status.get('weather_label','?')} | Zeit: {status.get('time_label','?')} ]",
        f"[ Mond: {moon_scale(status.get('moon_label','?'))} {status.get('moon_label','?')} | Venus: {venus_scale(status.get('venus_label','?'))} {status.get('venus_label','?')} | Aktion: {action} | Auto-Battle: {'an' if status.get('auto_battle_enabled') else 'aus'} | {compact_matrix_health_hint(matrix_snapshot)} ]",
    ]
    return [fit_plain_terminal_line(line, width) for line in lines]


@dataclass
class LiveContext:
    # Bündelt den letzten Snapshot und den visuellen Spinnerstand für sichere, serielle Redraws.
    snapshot: dict
    spinner_index: int = 0
    last_media_file: str = ""
    matrix_snapshot: dict[str, Any] | None = None
    last_matrix_refresh_ts: float = 0.0


def refresh_matrix_health(api: ApiClient, context: LiveContext, force: bool = False) -> None:
    now = time.time()
    if not force and context.last_matrix_refresh_ts > 0.0:
        if now - context.last_matrix_refresh_ts < MATRIX_HEALTH_REFRESH_SECONDS:
            return
    try:
        context.matrix_snapshot = api.matrix_health()
    except Exception:
        if context.matrix_snapshot is None:
            context.matrix_snapshot = {"health": {"status": "unavailable", "reason": "matrix-unreachable"}}
    finally:
        context.last_matrix_refresh_ts = now


# Holt den aktuellen Serverzustand seriell und vermeidet nebenlaeufige Terminalschreiber waehrend der Eingabe.
def refresh_live_context(api: ApiClient, context: LiveContext) -> None:
    context.snapshot = api.state()
    context.spinner_index = (context.spinner_index + 1) % len(SPINNERS)
    refresh_matrix_health(api, context)


# Rendert HUD und Prompt kontrolliert oberhalb der Shell-Zeile und kuerzt dabei alle UI-Zeilen auf die Terminalbreite.
def render_live_prompt(renderer: ReservedTerminalRenderer, context: LiveContext, cwd: Path) -> None:
    columns = renderer.terminal_size().columns
    renderer.reserve(HEADER_ROWS)
    renderer.draw_above_anchor(
        compact_status_lines(context.snapshot, context.spinner_index, columns, matrix_snapshot=context.matrix_snapshot),
        HEADER_ROWS,
    )
    renderer.write_prompt(format_shell_prompt(cwd, columns))


# Erkennt optionale Terminal-Bildrenderer und gibt deren Namen zurück.
def detect_media_renderer() -> str | None:
    for tool in ["chafa", "viu"]:
        if shutil.which(tool):
            return tool
    return None


# Rendert eine Bilddatei nur dann im Terminal, wenn ein passendes Tool installiert ist; sonst bleibt die Ausgabe verborgen.
def maybe_render_media(renderer: str | None, media_file: str) -> str:
    if not renderer or not media_file:
        return ""
    path = Path(media_file)
    if not path.exists():
        return ""
    try:
        if renderer == "chafa":
            result = subprocess.run([renderer, str(path), "--size=36x10"], capture_output=True, text=True, timeout=4)
            return result.stdout.strip()
        if renderer == "viu":
            result = subprocess.run([renderer, "-w", "36", str(path)], capture_output=True, text=True, timeout=4)
            return result.stdout.strip()
    except Exception:
        return ""
    return ""


# Zeigt nach einem Kommando nur die relevanten Detailblöcke an, statt jedes Mal den gesamten Snapshot zu scrollen.
def print_command_feedback(snapshot: dict, command: str, renderer: str | None) -> None:
    low = command.lower().strip()
    print(snapshot.get("message", ""))
    if snapshot.get("control_conflict"):
        print("Hinweis: Nutze 'control take', wenn diese Sitzung die aktive Steuerung explizit uebernehmen soll.")
        print(format_control_status(snapshot))
    for chunk in snapshot.get("stream_chunks", []):
        print(chunk)
    if low.startswith(("map", "explore")):
        print(render_map(snapshot["map_tiles"]))
    elif low.startswith(("inventory", "equip")):
        print(render_inventory(snapshot["inventory"]))
        print(render_equipment(snapshot["equipment"]))
    elif low.startswith(("market", "npc buy", "npc service")):
        print(render_market(snapshot["market"]))
    elif low.startswith(("city", "garrison", "militia")):
        print(render_city(snapshot.get("city")))
    elif low.startswith(("quest", "npc quest")):
        print(render_quests(snapshot.get("quests", [])))
    elif low.startswith(("journal", "talk", "townfolk")):
        print(render_journal(snapshot["journal"]))
    elif low.startswith(("attack", "guard", "dodge", "cast", "summon", "hunt")):
        print(render_combat(snapshot.get("combat", [])))
        print(render_buffs(snapshot.get("buffs", [])))
    media_preview = maybe_render_media(renderer, snapshot.get("status", {}).get("media_terminal_file", ""))
    if media_preview:
        print(media_preview)


# Führt den Hauptloop des Clients aus und verbindet Shell-Kommandos, Spielkommandos, Intro und Charaktererstellung.
def main(argv: list[str] | None = None) -> int:
    enable_ansi_support()
    renderer = ReservedTerminalRenderer()
    parser = argparse.ArgumentParser(description=f"ShellRPG terminal Phase {RELEASE_VERSION} client")
    parser.add_argument("--server", default="http://127.0.0.1:8765", help="Basis-URL des ShellRPG-Servers.")
    parser.add_argument("--command", help="Führt genau ein Spielkommando aus und beendet sich dann.")
    parser.add_argument("--skip-intro", action="store_true", help="Überspringt Intro und Fake-Boot, nützlich für Tests.")
    parser.add_argument("--new-character", action="store_true", help="Erzwingt die Charaktererstellung auch dann, wenn bereits ein Profil existiert.")
    args = parser.parse_args(argv)

    run_fake_boot(args.skip_intro, renderer=renderer)
    profile = None if args.new_character else read_profile()
    provisional_name = (profile or {}).get("character_name", "Neowulf")
    player_account_id = str((profile or {}).get("player_account_id", ""))
    device_id = str((profile or {}).get("device_id", ""))
    current_cwd = Path.cwd()

    try:
        api = ApiClient(
            args.server,
            character_name=provisional_name,
            player_account_id=player_account_id,
            device_id=device_id or None,
        )
    except Exception as exc:
        print(f"Server nicht erreichbar / Server unreachable: {exc}")
        print(r"PowerShell-Aktivierung: .\.venv\Scripts\Activate.ps1")
        print("Starte zuerst den privaten ShellRPG-server oder nutze den dedizierten Webzugang ueber ShellRPG-www.")
        return 1

    if profile is None or args.new_character:
        if args.command and not sys.stdin.isatty():
            profile = {
                "character_name": provisional_name or "Neowulf",
                "faction": "Menschen",
                "race_name": "Mensch",
                "class_name": "Ritter",
                "attributes": {"strength": 12, "dexterity": 11, "accuracy": 11, "intelligence": 10, "wisdom": 10, "speed": 10},
                "language": "de",
            }
        else:
            profile = run_character_creation("de", renderer=renderer, cwd=current_cwd)
        try:
            bootstrap_control = api.state()
            if not control_write_allowed(bootstrap_control):
                takeover = api.take_control("terminal-bootstrap-character-create")
                print(takeover.get("message", "Steuerung fuer die Charaktererstellung uebernommen."))
            api.create_character(profile)
            profile["player_account_id"] = api.player_account_id
            profile["device_id"] = api.device_id
            write_profile(profile)
        except Exception as exc:
            print(f"Charaktererstellung fehlgeschlagen: {exc}")
            return 1

    try:
        bootstrap = api.state()
    except Exception as exc:
        print(f"Serverzustand konnte nicht geladen werden: {exc}")
        return 1

    profile = sync_profile_identity(dict(profile or {"character_name": api.character_name}), api, snapshot=bootstrap)
    write_profile(profile)

    context = LiveContext(snapshot=bootstrap)
    refresh_matrix_health(api, context, force=True)

    if args.command:
        if is_character_command(args.command):
            handled, profile, snapshot = handle_character_command(
                args.command,
                api,
                profile,
                current_snapshot=context.snapshot,
                renderer=renderer,
                cwd=current_cwd,
            )
            if handled:
                if snapshot is not None:
                    context.snapshot = snapshot
                profile = sync_profile_identity(profile, api, snapshot=context.snapshot)
                write_profile(profile)
                return 0
        if handle_matrix_command(args.command, api):
            return 0
        handled, snapshot = handle_control_command(args.command, api)
        if handled:
            if snapshot is not None:
                context.snapshot = snapshot
                profile = sync_profile_identity(profile, api, snapshot=context.snapshot)
                write_profile(profile)
            return 0
        if is_game_command(args.command) and not is_observer_safe_game_command(context.snapshot, args.command) and guard_observer_write(context.snapshot, args.command):
            return 0
        snapshot = api.post_command(args.command)
        print_command_feedback(snapshot, args.command, detect_media_renderer())
        return 0

    cwd = current_cwd
    media_renderer = detect_media_renderer()
    print(color("Spielbefehle und Shell-Befehle teilen sich jetzt denselben Prompt. 'quit' oder 'exit' beendet nur den Client.", "90"))
    while True:
        try:
            refresh_live_context(api, context)
        except Exception:
            pass
        render_live_prompt(renderer, context, cwd)
        raw = input("").strip()
        if raw.lower() in {"quit", "exit"}:
            print("Sitzung beendet.")
            return 0
        if not raw:
            continue
        handled, profile, snapshot = handle_character_command(
            raw,
            api,
            profile,
            current_snapshot=context.snapshot,
            renderer=renderer,
            cwd=cwd,
        )
        if handled:
            if snapshot is not None:
                context.snapshot = snapshot
                context.spinner_index = (context.spinner_index + 1) % len(SPINNERS)
            profile = sync_profile_identity(profile, api, snapshot=context.snapshot)
            write_profile(profile)
            continue
        if handle_matrix_command(raw, api):
            continue
        control_handled, snapshot = handle_control_command(raw, api)
        if control_handled:
            if snapshot is not None:
                context.snapshot = snapshot
                context.spinner_index = (context.spinner_index + 1) % len(SPINNERS)
                profile = sync_profile_identity(profile, api, snapshot=context.snapshot)
                write_profile(profile)
            continue
        if is_game_command(raw):
            if not is_observer_safe_game_command(context.snapshot, raw) and guard_observer_write(context.snapshot, raw):
                continue
            snapshot = api.post_command(raw)
            context.snapshot = snapshot
            context.spinner_index = (context.spinner_index + 1) % len(SPINNERS)
            print_command_feedback(snapshot, raw, media_renderer)
            continue
        cwd, shell_output = run_shell_command(raw, cwd, capture_output=False)
        if shell_output:
            print(shell_output)
        else:
            sys.stdout.write("\n")
            sys.stdout.flush()
        try:
            refresh_live_context(api, context)
        except Exception:
            pass
