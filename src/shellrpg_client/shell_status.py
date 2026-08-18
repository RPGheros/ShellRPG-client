from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from shellrpg_client.api_client import ApiClient


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shellrpg-status",
        description="Print the authenticated ShellRPG status as exactly three lines.",
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:8765")
    parser.add_argument("--character-name", default="Ander")
    parser.add_argument("--account-id", default="")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        api = ApiClient(
            base_url=args.base_url,
            character_name=args.character_name,
            player_account_id=args.account_id,
        )
        lines = api.status_text().splitlines()
    except (ConnectionError, OSError, ValueError):
        return 0
    if len(lines) != 3:
        return 0

    normalized = [" ".join(line.split()) for line in lines]
    sys.stdout.write("\n".join(normalized) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
