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
