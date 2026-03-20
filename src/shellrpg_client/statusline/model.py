from dataclasses import dataclass

@dataclass(frozen=True)
class StatusLineState:
    character_name: str
    class_name: str
    location_label: str
    active_action: str
    hp_current: int
    hp_max: int
    tick_value: int
    gold: int
    hunger: str
