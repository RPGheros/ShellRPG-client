from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class CommandSpec:
    name: str
    help_short: str
    role_min: str = "player"

BASE_COMMANDS: tuple[CommandSpec, ...] = (
    CommandSpec("look", "Beschreibt die unmittelbare Umgebung."),
    CommandSpec("inspect", "Vertieft die Sicht auf Ort, Ziel oder Spur."),
    CommandSpec("walk", "Startet eine Reiseaktion oder einen Routenauftrag."),
    CommandSpec("inventory", "Zeigt das aktuelle Inventar."),
    CommandSpec("showcommands", "Listet sichtbare Befehle im aktuellen Kontext."),
)

def visible_commands(role: str = "player") -> Iterable[CommandSpec]:
    if role == "review_admin":
        yield from BASE_COMMANDS
        yield CommandSpec("riddle-review-list", "Zeigt ausstehende Rätselreviews.", role_min="review_admin")
    else:
        yield from BASE_COMMANDS
