
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
    CommandSpec("walk north|south|west|east|x,y", "Bewegt dich zu einem benachbarten Tile oder Koordinatenziel."),
    CommandSpec("walk route <ziel>", "Nutze eine benannte Route zu Stadt, Front oder Kubus."),
    CommandSpec("hunt north|south|west|east|x,y", "Startet eine Jagd mit Live-Status und Reaktionsfenstern."),
    CommandSpec("gather iron|wood|gems|gold|x,y", "Sammelt gezielt Ressourcen und steuert bekannte Vorkommen an."),
    CommandSpec("explore", "Steuert automatisch die nächste verdeckte Region an."),
    CommandSpec("attack / guard / dodge", "Kampfentscheidungen während eines Reaktionsfensters."),
    CommandSpec("cast soul trap", "Belegt das Ziel im Kampf mit Seelenfalle."),
    CommandSpec("auto battle on|off|balanced|aggressive|defensive", "Aktiviert Auto-Battle oder wechselt sein Profil."),
    CommandSpec("craft --item sword --material iron", "Stellt Ausrüstung ohne Unterstriche im UI her."),
    CommandSpec("socket --slot weapon --gem ruby shard", "Sockelt einen Edelstein in Ausrüstung."),
    CommandSpec("enchant --slot weapon", "Verzaubert ein Ausrüstungsteil."),
    CommandSpec("soul forge --slot weapon --stone soulstone lesser", "Schmiedet eine Waffe mit einem Seelenstein um."),
    CommandSpec("merchant list / buy <item> / sell <item>", "Interagiert mit lokalen Händlern."),
    CommandSpec("city found <name>", "Gründet eine Stadt auf dem aktuellen Tile."),
    CommandSpec("city appoint governor <name>", "Ernennt oder ersetzt den Gouverneur."),
    CommandSpec("city appoint general <1-5> <name>", "Besetzt einen Generals-Slot."),
    CommandSpec("city build <building>", "Errichtet ein Gebäude auf dem aktuellen Tile."),
    CommandSpec("city doctrine <1-5> <balanced|aggressive|defensive|supply|drill|recon>", "Setzt die Doktrin eines Generals."),
    CommandSpec("city collect taxes|stores", "Zieht Steuern oder Lagergüter aus der Stadt ein."),
    CommandSpec("city pass <ticks>", "Lässt mehrere Welt-Ticks für Produktion und Konflikte vergehen."),
    CommandSpec("militia recruit <unit> [amount]", "Hebt Miliztruppen aus."),
    CommandSpec("militia status", "Zeigt Garnison und Milizlinien."),
    CommandSpec("garrison status | fortify | sortie", "Steuert Garnisonsbereitschaft und Reaktion in Belagerungen."),
    CommandSpec("faction attack", "Löst einen Testangriff der aktuellen Feindfraktion aus."),
    CommandSpec("cube enter / cube leave / cube say <frage>", "Sprich mit dem schwarzen Kubus."),
    CommandSpec("use <item>", "Verwendet Tränke, Schriftrollen oder Bücher."),
    CommandSpec("equip <item>", "Rüstet Waffen, Rüstungen oder Accessoires aus."),
    CommandSpec("read <item>", "Öffnet ein Buch und erlaubt Blättern mit book next/prev."),
    CommandSpec("inventory", "Zeigt das aktuelle Inventar."),
    CommandSpec("equipment", "Zeigt ausgerüstete Gegenstände."),
    CommandSpec("market", "Zeigt den lokalen Markt mit Silber-/Goldpreisen."),
    CommandSpec("buffs", "Zeigt laufende Buffs."),
    CommandSpec("journal", "Zeigt die letzten Journal-Einträge."),
    CommandSpec("show commands", "Listet sichtbare Befehle im aktuellen Kontext."),
)

def visible_commands(role: str = "player") -> Iterable[CommandSpec]:
    yield from BASE_COMMANDS
