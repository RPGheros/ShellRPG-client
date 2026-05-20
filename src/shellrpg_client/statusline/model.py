from dataclasses import dataclass, field


@dataclass(frozen=True)
class StatusLineState:
    character_name: str
    class_name: str
    race_name: str
    level: int
    location_label: str
    coords_label: str
    active_action: str
    hp_current: int
    hp_max: int
    mana_current: int
    mana_max: int
    tick_value: int
    silver: int
    gold: int
    hunger: str
    overlay_message: str
    media_file: str
    language: str
    reaction_seconds_left: int = 0
    combat_choices: list[str] = field(default_factory=list)
    faction_tension: str = ""
    dialogue_mode: bool = False
    dialogue_target: str = ""
    activity_eta_seconds: int = 0
    activity_tick_seconds: int = 1
    visible_status_pulse_seconds: int = 5
    activity_resource_type: str = ""
    idle_reward_eta_seconds: int = 0
