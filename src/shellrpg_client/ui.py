from __future__ import annotations

from shellrpg_client.statusline.model import StatusLineState
from shellrpg_client.statusline.spinner import render_spinner


def render_status(status: dict) -> str:
    state = StatusLineState(**status)
    return (
        f"[{state.character_name} | {state.class_name} | {state.location_label} | "
        f"HP {state.hp_current}/{state.hp_max} | Hunger: {state.hunger} | Gold: {state.gold} | "
        f"Aktion: {state.active_action} | Tick {state.tick_value}] {render_spinner(state.tick_value)}"
    )


def render_map(map_tiles: list[dict]) -> str:
    lines = ["Bekannte Karte:"]
    for tile in map_tiles:
        marker = "*" if tile.get("is_current") else "-"
        lines.append(f"  {marker} {tile['label']} [{tile['visibility_state']}]")
    return "\n".join(lines)


def render_inventory(entries: list[dict]) -> str:
    lines = ["Inventar:"]
    for entry in entries:
        lines.append(f"  - {entry['item_name']} x{entry['quantity']}")
    return "\n".join(lines)


def render_market(entries: list[dict]) -> str:
    lines = ["Markt:"]
    for entry in entries:
        lines.append(f"  - {entry['item_name']}: {entry['price']} Gold ({entry['trend']})")
    return "\n".join(lines)


def render_journal(entries: list[str]) -> str:
    lines = ["Journal:"]
    for entry in entries[-5:]:
        lines.append(f"  - {entry}")
    return "\n".join(lines)
