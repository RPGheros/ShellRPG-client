from __future__ import annotations

import argparse
import threading
import time
from urllib.error import URLError

from shellrpg_client.api_client import ApiClient
from shellrpg_client.ui import (
    render_buffs,
    render_equipment,
    render_inventory,
    render_journal,
    render_map,
    render_market,
    render_overlay,
    render_quests,
    render_status,
)


def scrobble(chunks: list[str]) -> None:
    for chunk in chunks:
        print(chunk)
        time.sleep(0.15)


def print_snapshot(snapshot: dict) -> None:
    print(render_status(snapshot["status"]))
    print(render_overlay(snapshot["status"]))
    print(snapshot["message"])
    if snapshot.get("stream_chunks"):
        scrobble(snapshot["stream_chunks"])
    print(render_map(snapshot["map_tiles"]))
    print(render_inventory(snapshot["inventory"]))
    print(render_equipment(snapshot["equipment"]))
    print(render_market(snapshot["market"]))
    print(render_quests(snapshot["quests"]))
    print(render_buffs(snapshot["buffs"]))
    print(render_journal(snapshot["journal"]))


def start_live_monitor(api: ApiClient, stop_event: threading.Event) -> threading.Thread:
    def monitor() -> None:
        last_marker: tuple[int, str, str] | None = None
        while not stop_event.is_set():
            try:
                snapshot = api.state()
            except Exception:
                time.sleep(1.0)
                continue
            status = snapshot["status"]
            marker = (status["tick_value"], status["location_label"], status["overlay_message"])
            if marker != last_marker and status["active_action"] != "idle":
                print("\n[Live] " + render_status(status))
                print("[Live] " + status["overlay_message"])
                last_marker = marker
            time.sleep(1.0)
    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    return thread


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ShellRPG terminal Phase D client")
    parser.add_argument("--server", default="http://127.0.0.1:8765", help="Base URL of the local ShellRPG server.")
    parser.add_argument("--command", help="Run one command and exit.")
    args = parser.parse_args(argv)

    api = ApiClient(args.server)
    try:
        bootstrap = api.state()
    except URLError as exc:
        print(f"Server nicht erreichbar / Server unreachable: {exc}")
        print("Starte zuerst: python -m shellrpg_server")
        return 1

    print_snapshot(bootstrap)
    if args.command:
        snapshot = api.post_command(args.command)
        print()
        print_snapshot(snapshot)
        return 0

    stop_event = threading.Event()
    start_live_monitor(api, stop_event)
    print("\nType 'quit' oder 'exit' zum Beenden. Im Kubus-Dialog beendet '/leave' den Dialogmodus.\n")
    try:
        while True:
            try:
                status = api.state()["status"]
            except Exception:
                status = {"dialogue_mode": False}
            prompt = "cube> " if status.get("dialogue_mode") else "shellrpg> "
            raw = input(prompt).strip()
            if raw.lower() in {"quit", "exit"}:
                print("Sitzung beendet.")
                return 0
            if not raw:
                continue
            snapshot = api.post_command(raw)
            print()
            print_snapshot(snapshot)
            print()
    finally:
        stop_event.set()
