from dataclasses import dataclass, field


@dataclass(frozen=True)
class PublicCharacterStatus:
    character_name: str
    class_name: str
    hp_current: int
    hp_max: int
    location_label: str
    active_action: str
    tick_value: int
    gold: int
    hunger: str
    dialogue_mode: bool = False
    dialogue_target: str = ""
    combat_choices: list[str] = field(default_factory=list)
    reaction_seconds_left: int = 0
    activity_eta_seconds: int = 0
    activity_tick_seconds: int = 1
    visible_status_pulse_seconds: int = 5
    activity_resource_type: str = ""
    idle_reward_eta_seconds: int = 0
