from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class CommandSpec:
    name: str
    help_short: str
    role_min: str = "player"

BASE_COMMANDS: tuple[CommandSpec, ...] = (
    CommandSpec("look", "Beschreibt die aktuelle Umgebung."),
    CommandSpec("inspect", "Vertieft die Orts- und Pfadwahrnehmung."),
    CommandSpec("walk <richtung>", "Bewegt dich zu einem benachbarten Tile."),
    CommandSpec("walk route <ziel>", "Nutze eine benannte Kurzroute zu einer Stadt."),
    CommandSpec("map", "Zeigt die aktuell bekannte Kartenlage."),
    CommandSpec("inventory", "Zeigt das aktuelle Inventar."),
    CommandSpec("market", "Zeigt den lokalen Markt."),
    CommandSpec("journal", "Zeigt die letzten Journal-Einträge."),
    CommandSpec("gather", "Sammelt regionale Ressourcen."),
    CommandSpec("hunt", "Startet eine kurze Jagdaktion."),
    CommandSpec("explore", "Erkundet das aktuelle Tile intensiver."),
    CommandSpec("showcommands", "Listet sichtbare Befehle im aktuellen Kontext."),
)

def visible_commands(role: str = "player") -> Iterable[CommandSpec]:
    if role == "review_admin":
        yield from BASE_COMMANDS
        yield CommandSpec("riddle-review-list", "Zeigt ausstehende Rätselreviews.", role_min="review_admin")
    else:
        yield from BASE_COMMANDS
