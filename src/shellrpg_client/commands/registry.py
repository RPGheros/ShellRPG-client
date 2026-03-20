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
    CommandSpec("walk <N|S|W|O|x,y>", "Bewegt dich zu einem benachbarten Tile oder Koordinatenziel."),
    CommandSpec("walk route <ziel>", "Nutze eine benannte Route zu Stadt, Mine oder Kubus."),
    CommandSpec("hunt <N|S|W|O|x,y>", "Startet eine Jagd mit Live-Status und Reaktionsfenstern."),
    CommandSpec("gather wood|iron|gems|gold|x,y", "Sammelt gezielt Ressourcen und steuert bekannte Vorkommen an."),
    CommandSpec("explore", "Steuert automatisch die nächste verdeckte Region an."),
    CommandSpec("attack / guard / dodge", "Kampfentscheidungen während eines Reaktionsfensters."),
    CommandSpec("cast soultrap", "Belegt das Ziel im Kampf mit Seelenfalle."),
    CommandSpec("craft <recipe>", "Stellt ein Rezept her."),
    CommandSpec("socket weapon|armor|accessory <gem>", "Sockelt einen Edelstein in Ausrüstung."),
    CommandSpec("enchant weapon|armor|accessory", "Verzaubert ein Ausrüstungsteil."),
    CommandSpec("soulforge weapon [soulstone]", "Schmiedet eine Waffe mit einem Seelenstein um."),
    CommandSpec("merchant list / buy <item> / sell <item>", "Interagiert mit lokalen Händlern."),
    CommandSpec("cube enter / cube leave / cube say <frage>", "Sprich mit dem schwarzen Kubus."),
    CommandSpec("use <item>", "Verwendet Tränke, Schriftrollen oder Bücher."),
    CommandSpec("equip <item>", "Rüstet Waffen, Rüstungen oder Accessoires aus."),
    CommandSpec("read <item>", "Öffnet ein Buch und erlaubt Blättern mit book next/prev."),
    CommandSpec("inventory", "Zeigt das aktuelle Inventar."),
    CommandSpec("equipment", "Zeigt ausgerüstete Gegenstände."),
    CommandSpec("market", "Zeigt den lokalen Markt mit Silber-/Goldpreisen."),
    CommandSpec("quests", "Zeigt aktive Questketten."),
    CommandSpec("buffs", "Zeigt laufende Buffs."),
    CommandSpec("journal", "Zeigt die letzten Journal-Einträge."),
    CommandSpec("showcommands", "Listet sichtbare Befehle im aktuellen Kontext."),
)


def visible_commands(role: str = "player") -> Iterable[CommandSpec]:
    yield from BASE_COMMANDS
