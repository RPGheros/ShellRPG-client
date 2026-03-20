from __future__ import annotations

import argparse
from urllib.error import URLError

from shellrpg_client.api_client import ApiClient
from shellrpg_client.ui import render_inventory, render_journal, render_map, render_market, render_status


def print_snapshot(snapshot: dict) -> None:
    print(render_status(snapshot["status"]))
    print(snapshot["message"])
    print(render_map(snapshot["map_tiles"]))
    print(render_inventory(snapshot["inventory"]))
    print(render_market(snapshot["market"]))
    print(render_journal(snapshot["journal"]))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ShellRPG terminal Phase B client")
    parser.add_argument("--server", default="http://127.0.0.1:8765", help="Base URL of the local ShellRPG server.")
    parser.add_argument("--command", help="Run one command and exit.")
    args = parser.parse_args(argv)

    api = ApiClient(args.server)
    try:
        bootstrap = api.get("/api/help")
    except URLError as exc:
        print(f"Server nicht erreichbar: {exc}")
        print("Starte zuerst: python -m shellrpg_server")
        return 1

    print_snapshot(bootstrap)
    if args.command:
        snapshot = api.post_command(args.command)
        print()
        print_snapshot(snapshot)
        return 0

    print("\nType 'quit' oder 'exit' zum Beenden.\n")
    while True:
        raw = input("shellrpg> ").strip()
        if raw.lower() in {"quit", "exit"}:
            print("Sitzung beendet.")
            return 0
        if not raw:
            continue
        snapshot = api.post_command(raw)
        print()
        print_snapshot(snapshot)
        print()
