from __future__ import annotations

from shellrpg_client.statusline.model import StatusLineState
from shellrpg_client.statusline.spinner import render_spinner


def render_status(status: dict) -> str:
    state = StatusLineState(**status)
    extras = f" | Fenster {state.reaction_seconds_left}s" if state.reaction_seconds_left else ""
    dialogue = f" | Dialog: {state.dialogue_target}" if getattr(state, "dialogue_mode", False) else ""
    return (
        f"[{state.character_name} | {state.class_name}/{state.race_name} | Lvl {state.level} | "
        f"{state.location_label} [{state.coords_label}] | HP {state.hp_current}/{state.hp_max} | "
        f"MP {state.mana_current}/{state.mana_max} | {state.gold}g/{state.silver}s | Hunger: {state.hunger} | "
        f"Aktion: {state.active_action}{extras}{dialogue} | Tick {state.tick_value}] {render_spinner(state.tick_value)}"
    )


def render_overlay(status: dict) -> str:
    state = StatusLineState(**status)
    lines = [f"Overlay: {state.overlay_message}", f"Media: media/gifs/{state.media_file}"]
    if state.faction_tension:
        lines.append(f"Spannung: {state.faction_tension}")
    if state.combat_choices:
        lines.append("Reaktionsfenster: " + ", ".join(state.combat_choices))
    if getattr(state, "dialogue_mode", False):
        lines.append(f"Dialogmodus aktiv: {state.dialogue_target}")
    return "\n".join(lines)


def render_map(map_tiles: list[dict]) -> str:
    lines = ["Kartenausschnitt:"]
    for tile in map_tiles:
        marker = "*" if tile.get("is_current") else "-"
        poi = f" | POI: {', '.join(tile['poi_known'])}" if tile.get("poi_known") else ""
        resources = f" | Ressourcen: {', '.join(tile['known_resources'])}" if tile.get("known_resources") else ""
        lines.append(f"  {marker} {tile['label']} [{tile['coords_label']}] [{tile['visibility_state']}]" + poi + resources)
    return "\n".join(lines)


def render_inventory(entries: list[dict]) -> str:
    lines = ["Inventar:"]
    for entry in entries:
        affix = f" | {'; '.join(entry['affixes'])}" if entry.get('affixes') else ""
        lines.append(f"  - {entry['item_name']} x{entry['quantity']} [{entry['category']}/{entry['quality']}]" + affix)
    return "\n".join(lines)


def render_equipment(entries: list[dict]) -> str:
    lines = ["Ausrüstung:"]
    for entry in entries:
        affix = f" | {'; '.join(entry['affixes'])}" if entry.get('affixes') else ""
        lines.append(f"  - {entry['slot']}: {entry['item_name']} [{entry['quality']}]" + affix)
    return "\n".join(lines)


def render_market(entries: list[dict]) -> str:
    lines = ["Händler:"]
    for entry in entries:
        lines.append(f"  - {entry['item_name']}: {entry['price_display']} ({entry['trend']})")
    return "\n".join(lines)


def render_journal(entries: list[str]) -> str:
    lines = ["Journal:"]
    for entry in entries[-10:]:
        lines.append(f"  - {entry}")
    return "\n".join(lines)


def render_quests(entries: list[dict]) -> str:
    lines = ["Questlog:"]
    for entry in entries:
        lines.append(f"  - {entry['title']} [{entry['status']}] {entry['progress_text']} — {entry['description']}")
    return "\n".join(lines)


def render_buffs(entries: list[dict]) -> str:
    lines = ["Buffs:"]
    if not entries:
        lines.append("  - keine")
        return "\n".join(lines)
    for entry in entries:
        lines.append(f"  - {entry['buff_name']} +{entry['value']} ({entry['remaining_ticks']} Ticks) via {entry['source']}")
    return "\n".join(lines)
