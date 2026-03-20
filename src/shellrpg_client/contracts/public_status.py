from dataclasses import dataclass

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
