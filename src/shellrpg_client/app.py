# ShellRPG Datei-Banner | Terminal-Client v0.7.6 | Deutsch kommentiert
from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover - optionale Komfortabhängigkeit
    psutil = None

from shellrpg_client.api_client import ApiClient
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


# Zeigt eine harmlose, rein simulierte Prozedur zum fehlgeschlagenen Geräte- und Protokollzugriff an.
def run_probe_sequence(targets: list[dict[str, str]], glitch: bool = False) -> None:
    for target in targets:
        label = f"[{target['kind'].upper():>7}] {target['label']}"
        sys.stdout.write(color(label + "  ", "90"))
        sys.stdout.flush()
        for spinner in ["⠁", "⠂", "⠄", "⠂"]:
            sys.stdout.write(color(spinner, "36"))
            sys.stdout.flush()
            time.sleep(0.08 if glitch else 0.11)
            sys.stdout.write("\b")
        suffix = color("FEHLSCHLAG", "31")
        if glitch and random.random() < 0.35:
            suffix = color("VERWORFEN", "31")
        print(suffix)


# Erzeugt einen flüssigen Glitch-Text, der einzelne Zeichen kurzzeitig durch Symbole ersetzt.
def animate_glitch_text(text: str, frames: int = 45, center: bool = True) -> None:
    width = shutil.get_terminal_size((100, 30)).columns
    glyphs = "#@$%&*?!/\\|[]{}<>~^_-="
    for step in range(frames):
        chars = list(text)
        strength = 0.15 + (step / max(frames, 1)) * 0.25
        for idx, char in enumerate(chars):
            if char != " " and random.random() < strength:
                chars[idx] = random.choice(glyphs)
        render = "".join(chars)
        if center:
            offset = max(0, width // 2 - len(text) // 2 + (1 if step % 2 == 0 else -1))
            render = " " * offset + render
        sys.stdout.write("\r" + color(render, "35"))
        sys.stdout.flush()
        time.sleep(1 / 60)
    final = text.center(width) if center else text
    sys.stdout.write("\r" + color(final, "35") + "\n")
    sys.stdout.flush()


# Simuliert menschliches Tippen mit leichtem Jitter und optionalem Spinner am Ende.
def type_line(text: str, spinner_seconds: float = 0.0) -> None:
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02 + random.random() * 0.04)
    if spinner_seconds > 0:
        deadline = time.time() + spinner_seconds
        idx = 0
        while time.time() < deadline:
            sys.stdout.write(" " + SPINNERS[idx % len(SPINNERS)])
            sys.stdout.flush()
            time.sleep(0.15)
            sys.stdout.write("\b" * (len(SPINNERS[idx % len(SPINNERS)]) + 1) + " " * (len(SPINNERS[idx % len(SPINNERS)]) + 1) + "\b" * (len(SPINNERS[idx % len(SPINNERS)]) + 1))
            idx += 1
    sys.stdout.write("\n")
    sys.stdout.flush()


# Löscht eine Zeile wie bei gedrückt gehaltener Backspace-Taste wieder aus dem Terminal.
def erase_line(text: str) -> None:
    for _ in text:
        sys.stdout.write("\b \b")
        sys.stdout.flush()
        time.sleep(0.012 + random.random() * 0.02)
    sys.stdout.write("\n")
    sys.stdout.flush()


# Führt den atmosphärischen Fake-Boot-Prozess aus und berührt dabei keine externen Hosts.
def run_fake_boot(skip_intro: bool) -> None:
    if skip_intro:
        return
    print(color("== ShellRPG Initiation Bootstrap ==", "36"))
    targets = local_probe_targets()
    run_probe_sequence(targets, glitch=False)
    animate_glitch_text("Versuche Zugriff zu erhalten, umgehe Sicherheitsvorschriften.")
    run_probe_sequence(targets, glitch=True)
    print()
    phrase = "Autsch ... was war das?! Was ist gerade passiert?!"
    type_line(phrase, spinner_seconds=0.7)
    erase_line(phrase)
    type_line("Wo bin ich?!", spinner_seconds=0.6)
    erase_line("Wo bin ich?!")
    width = shutil.get_terminal_size((80, 25)).columns
    for _ in range(12):
        sys.stdout.write("\r" + " " * (width // 2) + color("_", "37"))
        sys.stdout.flush()
        time.sleep(0.25)
        sys.stdout.write("\r" + " " * (width // 2 + 1))
        sys.stdout.flush()
        time.sleep(0.15)
    type_line("Wer bin ich?!", spinner_seconds=0.5)
    print()


# Fragt eine Auswahl aus einer Liste ab und gibt den gewählten Wert zurück.
def choose_from_list(title: str, options: list[str]) -> str:
    print(title)
    for idx, option in enumerate(options, start=1):
        print(f"  {idx}. {option}")
    while True:
        raw = input("> ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print("Bitte eine gültige Zahl eingeben.")


# Liest eine freie Namenseingabe für den Charakter und begrenzt sie auf 32 Zeichen.
def ask_name() -> str:
    while True:
        name = input("Charaktername (max. 32 Zeichen): ").strip()
        if 1 <= len(name) <= 32:
            return name
        print("Bitte einen Namen zwischen 1 und 32 Zeichen eingeben.")


# Fragt Attributpunkte ab und verteilt sie in einem einfachen, aber belastbaren Einstiegsmenü.
def allocate_attributes(points: int = 12) -> dict[str, int]:
    base = {"strength": 10, "dexterity": 10, "accuracy": 10, "intelligence": 10, "wisdom": 10, "speed": 10}
    keys = list(base.keys())
    while points > 0:
        print(f"Verbleibende Attributpunkte: {points}")
        for idx, key in enumerate(keys, start=1):
            print(f"  {idx}. {key}: {base[key]}")
        raw = input("Punkt verteilen (Nummer oder Enter zum Abschließen): ").strip()
        if not raw:
            break
        if raw.isdigit() and 1 <= int(raw) <= len(keys):
            base[keys[int(raw)-1]] += 1
            points -= 1
        else:
            print("Ungültige Auswahl.")
    return base


# Führt die Charaktererstellung lokal aus und liefert das serverfähige Profil zurück.
def run_character_creation(default_language: str = "de") -> dict[str, Any]:
    print(color("=== Charaktererstellung ===", "33"))
    name = ask_name()
    faction = choose_from_list("Wähle deine Fraktion:", CHARACTER_FACTIONS)
    race = choose_from_list("Wähle deine Rasse:", CHARACTER_RACES)
    clazz = choose_from_list("Wähle deine Kampfklasse:", CHARACTER_CLASSES)
    attrs = allocate_attributes(12)
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
        payload = run_character_creation(str(current_profile.get("language", "de") or "de"))
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


# Erkennt, ob der eingegebene Text als Spielkommando und nicht als normales Shell-Kommando behandelt werden soll.
def is_game_command(raw: str) -> bool:
    if not raw:
        return False
    first = raw.strip().split()[0].lower()
    return first in GAME_VERBS


# Führt einfache Shell-Kommandos aus und behandelt Verzeichniswechsel lokal im Client-Prozess.
def run_shell_command(raw: str, cwd: Path) -> tuple[Path, str]:
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
        result = subprocess.run(stripped, shell=True, cwd=str(cwd), capture_output=True, text=True)
        output = (result.stdout or "") + (result.stderr or "")
        return cwd, output.strip() or f"Rückgabecode: {result.returncode}"
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


# Erzeugt die vier kompakten Statuszeilen für die nicht scrollende Live-Anzeige.
def compact_status_lines(snapshot: dict, spinner_index: int) -> list[str]:
    status = snapshot["status"]
    action = status.get("active_action", "idle")
    overlay = status.get("overlay_message", "")
    location = status.get("location_label", "?")
    if action in {"idle", ""}:
        live = f"Dein Ritter macht gerade nichts ... {SPINNERS[spinner_index % len(SPINNERS)]} [{location}]"
    else:
        live = f"{overlay} {SPINNERS[spinner_index % len(SPINNERS)]}"
    return [
        live,
        f"[ {status['character_name']} | {status['class_name']}/{status['race_name']} | Lvl {status['level']} | {location} [{status['coords_label']}] | HP {status['hp_current']}/{status['hp_max']} | MP {status['mana_current']}/{status['mana_max']} ]",
        f"[ {status['gold']} Gold / {status['silver']} Silber | Hunger: {status['hunger']} | Wetter: {status.get('weather_label','?')} | Zeit: {status.get('time_label','?')} ]",
        f"[ Mond: {moon_scale(status.get('moon_label','?'))} {status.get('moon_label','?')} | Venus: {venus_scale(status.get('venus_label','?'))} {status.get('venus_label','?')} | Aktion: {action} | Auto-Battle: {'an' if status.get('auto_battle_enabled') else 'aus'} ]",
    ]


@dataclass
class LiveContext:
    # Bündelt die laufenden Zustände für Header, Renderer und Hintergrundmonitor des Clients.
    snapshot: dict
    spinner_index: int = 0
    last_media_file: str = ""


class HeaderRenderer:
    # Zeichnet die kompakte Vierzeilen-Anzeige oberhalb des Shell-Prompts ohne Scroll-Spam neu.
    def __init__(self, rows: int = HEADER_ROWS) -> None:
        self.rows = rows
        self.lock = threading.Lock()

    # Reserviert Leerzeilen vor dem Prompt, damit die Live-Anzeige darüber Platz hat.
    def reserve(self) -> None:
        sys.stdout.write("\n" * self.rows)
        sys.stdout.flush()

    # Rendert die aktuelle Live-Anzeige mit ANSI-Cursorsteuerung über die reservierten Zeilen neu.
    def draw(self, lines: list[str]) -> None:
        with self.lock:
            sys.stdout.write("\x1b[s")
            sys.stdout.write(f"{ANSI}{self.rows}A")
            for idx in range(self.rows):
                sys.stdout.write(f"{ANSI}2K\r")
                sys.stdout.write((lines[idx] if idx < len(lines) else "") + ("\n" if idx < self.rows - 1 else ""))
            sys.stdout.write("\x1b[u")
            sys.stdout.flush()


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


# Aktualisiert den kompakten Header im Hintergrund sekündlich, während der Benutzer am Prompt arbeiten kann.
def start_live_monitor(api: ApiClient, context: LiveContext, renderer: HeaderRenderer, stop_event: threading.Event) -> threading.Thread:
    def monitor() -> None:
        while not stop_event.is_set():
            try:
                context.snapshot = api.state()
                context.spinner_index = (context.spinner_index + 1) % len(SPINNERS)
                renderer.draw(compact_status_lines(context.snapshot, context.spinner_index))
            except Exception:
                pass
            time.sleep(1.0)
    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    return thread


# Führt den Hauptloop des Clients aus und verbindet Shell-Kommandos, Spielkommandos, Intro und Charaktererstellung.
def main(argv: list[str] | None = None) -> int:
    enable_ansi_support()
    parser = argparse.ArgumentParser(description=f"ShellRPG terminal Phase {RELEASE_VERSION} client")
    parser.add_argument("--server", default="http://127.0.0.1:8765", help="Basis-URL des ShellRPG-Servers.")
    parser.add_argument("--command", help="Führt genau ein Spielkommando aus und beendet sich dann.")
    parser.add_argument("--skip-intro", action="store_true", help="Überspringt Intro und Fake-Boot, nützlich für Tests.")
    parser.add_argument("--new-character", action="store_true", help="Erzwingt die Charaktererstellung auch dann, wenn bereits ein Profil existiert.")
    args = parser.parse_args(argv)

    run_fake_boot(args.skip_intro)
    profile = None if args.new_character else read_profile()
    provisional_name = (profile or {}).get("character_name", "Neowulf")
    player_account_id = str((profile or {}).get("player_account_id", ""))
    device_id = str((profile or {}).get("device_id", ""))

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
            profile = run_character_creation("de")
        try:
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
    renderer = HeaderRenderer(HEADER_ROWS)
    renderer.reserve()
    renderer.draw(compact_status_lines(context.snapshot, context.spinner_index))

    if args.command:
        if is_character_command(args.command):
            handled, profile, snapshot = handle_character_command(args.command, api, profile)
            if handled:
                if snapshot is not None:
                    context.snapshot = snapshot
                profile = sync_profile_identity(profile, api, snapshot=context.snapshot)
                write_profile(profile)
                return 0
        snapshot = api.post_command(args.command)
        print_command_feedback(snapshot, args.command, detect_media_renderer())
        return 0

    cwd = Path.cwd()
    media_renderer = detect_media_renderer()
    stop_event = threading.Event()
    start_live_monitor(api, context, renderer, stop_event)
    print(color("Spielbefehle und Shell-Befehle teilen sich jetzt denselben Prompt. 'quit' oder 'exit' beendet nur den Client.", "90"))
    try:
        while True:
            prompt = f"PS {cwd}> "
            raw = input(prompt).strip()
            if raw.lower() in {"quit", "exit"}:
                print("Sitzung beendet.")
                return 0
            if not raw:
                continue
            handled, profile, snapshot = handle_character_command(raw, api, profile)
            if handled:
                if snapshot is not None:
                    context.snapshot = snapshot
                profile = sync_profile_identity(profile, api, snapshot=context.snapshot)
                write_profile(profile)
                renderer.reserve()
                renderer.draw(compact_status_lines(context.snapshot, context.spinner_index))
                continue
            if is_game_command(raw):
                snapshot = api.post_command(raw)
                context.snapshot = snapshot
                print_command_feedback(snapshot, raw, media_renderer)
                renderer.reserve()
                renderer.draw(compact_status_lines(context.snapshot, context.spinner_index))
                continue
            cwd, shell_output = run_shell_command(raw, cwd)
            if shell_output:
                print(shell_output)
            renderer.reserve()
            renderer.draw(compact_status_lines(context.snapshot, context.spinner_index))
    finally:
        stop_event.set()
