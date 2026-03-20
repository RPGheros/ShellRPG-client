# ShellRPG-client

**Governance:** CLIENT-PUBLIC  
**Visibility:** public  
**Version:** `v0.0.2`

Öffentlicher Terminal-Client für **Bauphase B / Vertical Slice**.

## Neu in diesem Stand

- `python -m shellrpg_client` funktioniert jetzt als echter Entrypoint
- interaktiver Terminal-Loop gegen den autoritativen lokalen Demo-Server
- Statuszeile, Karten-, Inventar-, Markt- und Journalausgabe
- Command-Bridge zu `look`, `inspect`, `walk`, `gather`, `hunt`, `explore`

## Start

```bash
python -m pip install -e .
python -m shellrpg_client
```

Optional mit Einzelbefehl:

```bash
python -m shellrpg_client --command "walk east"
```

## Voraussetzung

Der lokale Demo-Server aus `ShellRPG-server` muss laufen:

```bash
python -m shellrpg_server
```

## Revisionshinweis

- Foundations `0.0.1a` → **Phase B `0.0.2`** durch neue Funktionalität
- der Entrypoint-Fix selbst wäre für sich genommen versionsneutral gewesen; der gleichzeitige Vertical Slice rechtfertigt die neue Version
