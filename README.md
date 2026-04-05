<!-- ShellRPG Comment Banner | Revisionsänderung: Start-/Windows-/Timezone-Fix -->
Deutsch | [English](README.en.md)

🏛️☠️🌿                                                                 🌿☠️🏛️
╔══════════════════════════════════════════════════════════════════════════════╗
║  _/\______________________________________________________________/\\_     ║
║  \_/\\                                                            /\_/     ║
║  /_/\\   A U F G E R O L L T E   S C H R I F T R O L L E         /\_\     ║
║  \_\/____________________________________________________________\/_/     ║
╚══════════════════════════════════════════════════════════════════════════════╝
# ShellRPG-client · v0.7.6

## 1. Beschreibung

**Artefaktrolle:** Öffentlicher Terminal-Client für ShellRPG mit Shell-Eingabe, Statuszeile, Ereignislog, Kartenansicht und Medien-Fallbacks.

**Zweck:** Dieses Artefakt ist für die direkte Interaktion in Bash, Zsh, PowerShell oder kompatiblen Terminals gedacht. Es sendet Befehle an den Server und rendert den Rückkanal in einer shellfreundlichen Oberfläche.

**Verknüpfte Artefakte:**
- `ShellRPG-server` ist die autoritative Datenquelle.
- `ShellRPG-www` ist der grafische Schwester-Client für denselben Serverzustand.
- `ShellRPG-wiki` erklärt Befehle, Systeme und Begriffe für Nutzerinnen und Nutzer.

**Governance:** `CLIENT-PUBLIC`

## Pflegehinweis

- Bei relevanten Content-, Contract-, Feature- oder Redaktionsänderungen an
  diesem Endpunkt `README.md`, `README.en.md` und `VERSION` gemeinsam
  aktualisieren.

## 2. Abhängigkeiten

- Python 3.11 oder neuer
- pip
- laufender `ShellRPG-server` empfohlen
- Truecolor/ANSI optional, mit Fallback auf einfachere Darstellung

## 3. Installation

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # PowerShell
# Alternativ in CMD: .venv\Scripts\activate.bat
# Alternativ in Bash/Zsh: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m shellrpg_client
```

Der dedizierte Browserzugang läuft getrennt über `ShellRPG-www`.
Der Terminal-Client behaelt seine lokalen Medienpfade fuer GIF-/ASCII-Vorschau;
WWW-Bildpfade fuer Browseransichten laufen getrennt ueber den Web-/CDN-Pfad.

Aktuelle Kanonvorbereitung:
- kuenftige UI-Texte muessen Monster, Hive, Wildlife, Natur und Daemonen klar
  unterscheiden
- die Ausruestungsdarstellung wird auf sechs Ringslots pro Charakter
  vorbereitet
- wenn der Server redigierte Tile-Welthinweise liefert, zeigt die
  Kartenansicht jetzt unter der Karte ein `Milieu: ...`, statt dafuer einen
  separaten Client-Sonderpfad mit eigener Begriffswahrheit aufzubauen
- derselbe Kartenpfad kann jetzt auch einen redigierten `Stadthinweis: ...`
  aus `urban_suspicion_line` zeigen; die Terminaldarstellung bleibt dabei an
  den serverseitigen Public-Vertrag gebunden
- derselbe Kartenpfad kann jetzt auch eine redigierte
  `Stadtdiagnose: ...` aus dem persistierten urbanen Verdachtspool zeigen;
  Tile-Hinweis und Diagnose bleiben dabei an dieselben serverseitigen
  Registry-Refs gebunden
- der Terminal-Client besitzt jetzt zusaetzlich einen lokalen
  `matrix`-Befehlsbaum fuer `/api/matrix/health` und `/api/matrix/status`
  und kann damit dieselben Severity-, Konflikt-, Hotspot- und Peer-
  Diagnosedaten wie das WWW in shellfreundlicher Form anzeigen
- derselbe Matrixpfad kann Character-Konflikte jetzt lokal auch filtern
  (`matrix conflicts <filter>`) und gezielt per Charactername,
  `conflict_id` oder `field_conflict_id` drilldownen
  (`matrix inspect <...>`)
- der Drilldown zeigt Preferred-, Fallback- und Gemerged-Preview, Merge-
  Modus, Gewinnerseite sowie priorisierte Delta-Gruende direkt in der
  Terminalausgabe, statt nur die Kurzliste der Konflikte zu rendern
- dieselbe Matrix-Gesundheit erscheint jetzt auch als kompakter `Mx:`-
  Hinweis in der laufenden HUD-Zeile, ohne den Shell-Prompt oder den
  eigentlichen Spiel-Snapshot zu verdrängen

## 4. Feedback & Contribution

Feedback sollte immer das Terminalprofil, das Betriebssystem und den ausgeführten Befehl mit angeben.
Contribution ist willkommen, solange die Shell-Integrität, Fallback-Kette und Public/Private-Trennung gewahrt bleiben.
UI-Änderungen müssen möglichst in Deutsch und Englisch nachvollziehbar bleiben.

🏛️🌿☠️══════════════════════════════════════════════════════════════☠️🌿🏛️
