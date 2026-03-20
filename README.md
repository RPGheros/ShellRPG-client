# ShellRPG-client

**Governance:** `CLIENT-PUBLIC`  
**Release:** `v0.3.0`  
**Project version in TOML:** `0.3.0`

## Rolle
Öffentlicher Terminal-Client für denselben autoritativen Slice wie `ShellRPG-www`.

## Highlights in v0.3.0
- `python -m shellrpg_client` bleibt startbar
- Live-Status für `hunt`, `gather`, `explore`
- Reaktionsfenster im Kampf
- Crafting-/Socketing-/Enchanting-/Soulforge-Befehle
- Händlerbefehle
- Kubus-Dialogmodus mit `cube>`-Prompt
- GIF-Verlinkung passend zum aktuellen Tile oder Encounter

## Start
```bash
python -m pip install -e .
python -m shellrpg_client
```

Mit alternativem Server:
```bash
python -m shellrpg_client --server http://127.0.0.1:8765
```

## Kubus-Modus
- `walk route cube`
- `cube enter`
- danach wird jede Eingabe automatisch an den Kubus weitergereicht
- `/leave` oder `cube leave` beendet den Modus

## Medien
Die GIF-Dateien liegen unter:
- `media/gifs/`

Fehlende Rich-Media-Unterstützung ist nicht spielkritisch; der Client bleibt voll textspielbar.
