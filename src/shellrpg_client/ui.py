from __future__ import annotations


def format_countdown(seconds: int | float | str, *, combat: bool = False) -> str:
    try:
        total = max(0, int(float(seconds)))
    except (TypeError, ValueError):
        total = 0
    if combat and total <= 60:
        return f"00:{total:02d}"
    minutes, rest = divmod(total, 60)
    return f"{minutes:02d}:{rest:02d}"


def status_countdown(status: dict) -> str:
    if status.get("reaction_seconds_left"):
        return f"Combat: {format_countdown(status.get('reaction_seconds_left', 0), combat=True)}"
    if int(status.get("activity_eta_seconds") or 0) > 0:
        action = status.get("activity_type") or status.get("active_action") or "Aktion"
        resource = status.get("activity_resource_type") or ""
        labels = {
            "walk": "Reise",
            "gather": "Goldzyklus" if resource == "gold" else "Sammeln",
            "fish": "Angeln",
            "hunt": "Jagd",
            "explore": "Erkundung",
        }
        return f"{labels.get(action, str(action).title())}: {format_countdown(status.get('activity_eta_seconds', 0))}"
    if int(status.get("idle_reward_eta_seconds") or 0) > 0:
        return f"Idle-Drop: {format_countdown(status.get('idle_reward_eta_seconds', 0))}"
    return ""


def _slot_label(slot: str) -> str:
    return str(slot or "").replace("_", " ")


def render_status(status: dict) -> str:
    extras = f" | Fenster {status['reaction_seconds_left']}s" if status.get("reaction_seconds_left") else ""
    countdown = status_countdown(status)
    countdown_text = f" | Countdown {countdown}" if countdown else ""
    dialogue = f" | Dialog: {status['dialogue_target']}" if status.get("dialogue_mode") else ""
    auto = f" | Auto-Battle: {'an' if status.get('auto_battle_enabled') else 'aus'} ({status.get('auto_battle_mode','balanced')})"
    return (
        f"[{status['character_name']} | {status['class_name']}/{status['race_name']} | Lvl {status['level']} | "
        f"{status['location_label']} [{status['coords_label']}] | HP {status['hp_current']}/{status['hp_max']} | "
        f"MP {status['mana_current']}/{status['mana_max']} | {status['gold']}g/{status['silver']}s | Hunger: {status['hunger']} | "
        f"Wetter: {status.get('weather_label','?')} | Zeit: {status.get('time_label','?')} | Mond: {status.get('moon_label','?')} | Venus: {status.get('venus_label','?')} | "
        f"Aktion: {status['active_action']}{extras}{countdown_text}{dialogue}{auto} | Tick {status['tick_value']}]"
    )


def render_overlay(status: dict) -> str:
    lines = [
        f"Overlay: {status['overlay_message']}",
        f"Terminal-Media: {status.get('media_terminal_file','')}",
        f"WWW-Media: {status.get('media_file','')}",
        f"Server: {status.get('server_id','')} | Kalender: {status.get('calendar_source','')} | Boot-Save: {status.get('boot_savepoint_source','local')}@{status.get('boot_savepoint_tick',0)}",
    ]
    if status.get('weather_effects'):
        lines.append('Wettereffekte: ' + ' / '.join(status['weather_effects']))
    if status.get("faction_tension"):
        lines.append(f"Spannung: {status['faction_tension']}")
    if status.get("combat_choices"):
        lines.append("Reaktionsfenster: " + ", ".join(status["combat_choices"]))
    countdown = status_countdown(status)
    if countdown:
        lines.append(f"Countdown: {countdown}")
    return "\n".join(lines)


def render_map(map_tiles: list[dict]) -> str:
    lines = ["Kartenausschnitt:"]
    for tile in map_tiles:
        marker = "*" if tile.get("is_current") else "-"
        if tile['visibility_state'] == 'unknown':
            lines.append(f"  {marker} Unkartiert")
            continue
        parts = [f"  {marker} {tile['label']} [{tile['coords_label']}] [{tile['visibility_state']}]"]
        if tile.get("biome"):
            parts.append(f"{tile['biome']}/{tile.get('terrain','')}")
        if tile.get("spawn_milieu"):
            parts.append(f"Milieu: {tile['spawn_milieu']}")
        if tile.get("urban_suspicion_line"):
            parts.append(f"Stadthinweis: {tile['urban_suspicion_line']}")
        if tile.get("urban_diagnosis_line"):
            parts.append(f"Stadtdiagnose: {tile['urban_diagnosis_line']}")
        if tile.get("building"):
            parts.append(f"Bauwerk: {tile['building']}")
        if tile.get("known_resources"):
            parts.append("Ressourcen: " + ", ".join(tile["known_resources"]))
        lines.append(" | ".join(parts))
    return "\n".join(lines)


def render_inventory(entries: list[dict]) -> str:
    lines = ["Inventar:"]
    for entry in entries:
        affix = f" | {'; '.join(entry['affixes'])}" if entry.get('affixes') else ""
        lines.append(f"  - {entry['item_name']} x{entry['quantity']} [{entry['category']}/{entry['quality']}] | {entry.get('sprite','')}{affix}")
    return "\n".join(lines)


def render_equipment(entries: list[dict]) -> str:
    lines = ["Ausrüstung:"]
    for entry in entries:
        label = _slot_label(entry.get("slot", ""))
        if not entry.get("occupied", True):
            lines.append(f"  - {label}: [leer]")
            continue
        affix = f" | {'; '.join(entry['affixes'])}" if entry.get('affixes') else ""
        lines.append(f"  - {label}: {entry['item_name']} [{entry['quality']}] | {entry.get('sprite','')}{affix}")
    return "\n".join(lines)


def render_market(entries: list[dict]) -> str:
    lines = ["Händler:"]
    for entry in entries:
        lines.append(f"  - {entry['item_name']}: {entry['price_display']} ({entry['trend']})")
    return "\n".join(lines)


def render_journal(entries: list[str]) -> str:
    lines = ["Journal:"]
    for entry in entries[-12:]:
        lines.append(f"  - {entry}")
    return "\n".join(lines)


def render_quests(entries: list[dict]) -> str:
    lines = ["Questlog:"]
    if not entries:
        lines.append("  - keine aktiven Quests")
    for entry in entries:
        lines.append(f"  - {entry['title']} [{entry['status']}] {entry['progress_text']} — {entry['description']}")
    return "\n".join(lines)


def render_buffs(entries: list[dict]) -> str:
    lines = ["Buffs:"]
    if not entries:
        lines.append("  - keine")
        return "\n".join(lines)
    for entry in entries:
        lines.append(f"  - {entry['buff_name']} {entry['value']:+} ({entry['remaining_ticks']} Ticks) via {entry['source']}")
    return "\n".join(lines)


def render_combat(entries: list[dict]) -> str:
    lines = ["Kampf:"]
    if not entries:
        lines.append("  - kein aktiver Kampf")
        return "\n".join(lines)
    for entry in entries:
        lines.append(f"  - {entry['enemy_name']} HP {entry['hp_current']}/{entry['hp_max']} [{entry['faction']}/{entry['damage_type']}]")
    return "\n".join(lines)


def render_city(city: dict | None) -> str:
    lines = ["Stadt:"]
    if not city:
        lines.append("  - noch keine gegründete Stadt")
        return "\n".join(lines)
    lines.append(f"  - {city['city_name']} | Gouverneur: {city['governor_name']} | Steuern: {city['taxes_silver']}s | Bevölkerung: {city['population']} | Forschung: {city['research_points']}")
    if city.get('region_line'):
        lines.append(f"    Region: {city['region_line']}")
    if city.get('weather_pressure_line'):
        lines.append(f"    Wetter: {city['weather_pressure_line']}")
    if city.get('urban_suspicion_line'):
        lines.append(f"    Hinweis: {city['urban_suspicion_line']}")
    if city.get('urban_diagnosis_line'):
        lines.append(f"    Diagnose: {city['urban_diagnosis_line']}")
    for title, key in [("Bauwerke", 'building_lines'), ("Miliz", 'militia_lines'), ("Generäle", 'general_lines'), ("Produktion", 'production_lines'), ("Belagerung", 'siege_lines')]:
        if city.get(key):
            lines.append(f"  {title}:")
            lines.extend([f"    • {line}" for line in city[key]])
    return "\n".join(lines)
