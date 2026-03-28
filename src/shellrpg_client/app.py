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
import webbrowser
from dataclasses import dataclass
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
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
    "look", "inspect", "walk", "explore", "hunt", "gather", "inventory", "equip", "use", "trade", "party",
    "faction", "map", "quest", "pet", "help", "showcommands", "attack", "guard", "dodge", "cast", "summon",
    "npc", "artifact", "city", "garrison", "militia", "rcon", "market", "journal", "brew", "enchant", "craft",
    "townfolk", "server", "recovery", "weather", "auto", "book", "weave", "dialogue", "talk", "service",
}
ANSI = "\x1b["
SPINNERS = ["● ○ ○ ○ ○", "● ● ○ ○ ○", "● ● ● ○ ○", "● ● ● ● ○", "● ● ● ● ●"]


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
    faction = choose_from_list("Wähle deine Fraktion:", ["Menschen", "Amazonen", "Waldelfen", "Dryaden", "Baumwesen", "Nekari", "Ssarathi", "Salzlungen", "Orks", "Dämonen"])
    race = choose_from_list("Wähle deine Rasse:", ["Mensch", "Nekari", "Ssarathi", "Salzlunge", "Waldelf", "Dryade", "Baumwesen"])
    clazz = choose_from_list("Wähle deine Kampfklasse:", ["Ritter", "Totenbeschwörer", "Kleriker", "Waldläufer", "Magier", "Dieb", "Beastmaster"])
    attrs = allocate_attributes(12)
    return {
        "character_name": name,
        "faction": faction,
        "race_name": race,
        "class_name": clazz,
        "attributes": attrs,
        "language": default_language,
    }


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


# Startet einen eingebetteten WWW-Server für den Standalone-Modus und öffnet ihn im Browser.
def start_embedded_www(port: int) -> tuple[ThreadingHTTPServer, threading.Thread]:
    web_root = Path(__file__).resolve().parent / "embedded_www"

    class Handler(SimpleHTTPRequestHandler):
        # Liefert die eingebetteten Webdateien aus und unterdrückt Standard-Logging im Client.
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(web_root), **kwargs)

        # Unterdrückt das übliche HTTP-Logging im lokalen Standalone-Dashboard.
        def log_message(self, format, *args):
            return

    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, thread


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
    parser.add_argument("--standalone", action="store_true", help="Startet das eingebettete WWW-Dashboard und öffnet es im Browser.")
    parser.add_argument("--standalone-port", default=8088, type=int)
    parser.add_argument("--skip-intro", action="store_true", help="Überspringt Intro und Fake-Boot, nützlich für Tests.")
    parser.add_argument("--new-character", action="store_true", help="Erzwingt die Charaktererstellung auch dann, wenn bereits ein Profil existiert.")
    args = parser.parse_args(argv)

    run_fake_boot(args.skip_intro)
    profile = None if args.new_character else read_profile()
    provisional_name = (profile or {}).get("character_name", "Neowulf")

    try:
        api = ApiClient(args.server, character_name=provisional_name)
    except Exception as exc:
        print(f"Server nicht erreichbar / Server unreachable: {exc}")
        print(r"PowerShell-Aktivierung: .\.venv\Scripts\Activate.ps1")
        print("Starte zuerst: python -m shellrpg_server")
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
            write_profile(profile)
        except Exception as exc:
            print(f"Charaktererstellung fehlgeschlagen: {exc}")
            return 1
    else:
        try:
            api.create_character(profile)
        except Exception:
            pass

    try:
        bootstrap = api.state()
    except Exception as exc:
        print(f"Serverzustand konnte nicht geladen werden: {exc}")
        return 1

    httpd = None
    if args.standalone:
        httpd, _ = start_embedded_www(args.standalone_port)
        try:
            webbrowser.open(f"http://127.0.0.1:{args.standalone_port}/public/index.html", new=2)
        except Exception:
            pass
        print(f"Standalone-Dashboard aktiv auf http://127.0.0.1:{args.standalone_port}/public/index.html")

    context = LiveContext(snapshot=bootstrap)
    renderer = HeaderRenderer(HEADER_ROWS)
    renderer.reserve()
    renderer.draw(compact_status_lines(context.snapshot, context.spinner_index))

    if args.command:
        snapshot = api.post_command(args.command)
        print_command_feedback(snapshot, args.command, detect_media_renderer())
        if httpd:
            httpd.shutdown()
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
        if httpd:
            httpd.shutdown()
