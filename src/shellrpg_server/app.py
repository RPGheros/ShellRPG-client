
from __future__ import annotations
import argparse
from shellrpg_server.api.http import run_server

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ShellRPG private authoritative Phase E server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args(argv)
    run_server(args.host, args.port)
    return 0
