from dataclasses import dataclass

@dataclass(frozen=True)
class CharacterViewState:
    character_name: str
    class_name: str
    location_label: str
    active_action: str
    hp_current: int
    hp_max: int
    tick_value: int
    activity_eta_seconds: int = 0
    idle_reward_eta_seconds: int = 0
