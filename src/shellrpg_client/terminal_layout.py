# ShellRPG Datei-Banner | Terminal-Layout | Deutsch kommentiert
from __future__ import annotations

import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

ANSI = "\x1b["
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
ELLIPSIS = "..."


# Entfernt ANSI-Sequenzen, damit Breitenberechnungen nicht von Farb-Codes verfälscht werden.
def strip_ansi(text: str) -> str:
    return ANSI_PATTERN.sub("", text)


# Begrenzt einen Text auf eine sichtbare Zielbreite und hängt bei Bedarf eine Ellipse an.
def fit_text_width(text: str, max_visible: int) -> str:
    clean = strip_ansi(text).replace("\r", " ").replace("\n", " ")
    if max_visible <= 0:
        return ""
    if len(clean) <= max_visible:
        return clean
    if max_visible <= len(ELLIPSIS):
        return clean[:max_visible]
    return clean[: max_visible - len(ELLIPSIS)] + ELLIPSIS


# Füllt einen Text nach dem Kürzen auf eine feste sichtbare Breite auf.
def pad_text_width(text: str, max_visible: int, align: str = "left") -> str:
    fitted = fit_text_width(text, max_visible)
    if align == "center":
        return fitted.center(max_visible)
    if align == "right":
        return fitted.rjust(max_visible)
    return fitted.ljust(max_visible)


# Kürzt eine Terminalzeile so, dass sie garantiert innerhalb einer physischen Konsolenzeile bleibt.
def fit_plain_terminal_line(text: str, columns: int) -> str:
    return fit_text_width(text, max(1, columns - 1))


# Baut einen PowerShell-aehnlichen Prompt und kuerzt den Pfad notfalls von links.
def format_shell_prompt(cwd: Path, columns: int) -> str:
    prefix = "PS "
    suffix = "> "
    max_visible = max(1, columns - 1)
    available = max(1, max_visible - len(prefix) - len(suffix))
    path_text = str(cwd)
    if len(path_text) > available:
        if available <= len(ELLIPSIS):
            path_text = path_text[-available:]
        else:
            tail = max(1, available - len(ELLIPSIS))
            path_text = ELLIPSIS + path_text[-tail:]
    return fit_text_width(f"{prefix}{path_text}{suffix}", max_visible)


@dataclass
class ReservedTerminalRenderer:
    # Verwaltet einen festen Renderanker oberhalb der Eingabezeile, ohne die Prompt-Zeile selbst zu ueberschreiben.
    stream: TextIO = sys.stdout
    fallback_columns: int = 100
    fallback_lines: int = 30

    # Liest die aktuelle Terminalgroesse und faellt fuer Tests oder Pipes auf sichere Standardwerte zurueck.
    def terminal_size(self) -> os.terminal_size:  # type: ignore[name-defined]
        return shutil.get_terminal_size((self.fallback_columns, self.fallback_lines))

    # Reserviert Leerzeilen zwischen Verlauf und Prompt, damit die UI ausschliesslich dort gerendert wird.
    def reserve(self, rows: int) -> None:
        if rows <= 0:
            return
        self.stream.write("\n" * rows)
        self.stream.flush()

    # Rendert einen Block ueber dem zuletzt reservierten Anker und kehrt danach zur Eingabezeile zurueck.
    def draw_above_anchor(self, lines: list[str], rows: int) -> None:
        if rows <= 0:
            return
        self.stream.write("\x1b[s")
        self.stream.write(f"{ANSI}{rows}A")
        for idx in range(rows):
            self.stream.write(f"{ANSI}2K\r")
            self.stream.write(lines[idx] if idx < len(lines) else "")
            if idx < rows - 1:
                self.stream.write("\n")
        self.stream.write("\x1b[u")
        self.stream.flush()

    # Bereinigt die aktuelle Prompt-Zeile und schreibt den neuen Eingabeprompt kontrolliert an dieselbe Stelle.
    def write_prompt(self, prompt_text: str) -> None:
        self.stream.write(f"{ANSI}2K\r{prompt_text}")
        self.stream.flush()

    # Stellt nach einem Wizard-Schritt den Prompt-Anker wieder her, ohne den Verlauf zu verschieben.
    def reanchor_prompt_line(self) -> None:
        self.stream.write(f"{ANSI}1A\r")
        self.stream.flush()


class ReservedRenderSession:
    # Kapselt mehrere Redraws gegen denselben Anker, etwa fuer Intro- oder Schriftrollen-Animationen.
    def __init__(self, renderer: ReservedTerminalRenderer, rows: int) -> None:
        self.renderer = renderer
        self.rows = rows
        self.active = False

    # Startet die Session und reserviert den benoetigten UI-Bereich genau einmal.
    def __enter__(self) -> "ReservedRenderSession":
        self.renderer.reserve(self.rows)
        self.active = True
        return self

    # Rendert den aktuellen Frame ueber dem Anker und aktualisiert optional die Eingabezeile.
    def render(self, lines: list[str], prompt_text: str = "") -> None:
        if not self.active:
            raise RuntimeError("Render-Session ist nicht aktiv.")
        self.renderer.draw_above_anchor(lines[: self.rows], self.rows)
        self.renderer.write_prompt(prompt_text)

    # Liest eine Eingabe ueber denselben Prompt-Anker ein und stellt danach den Zeichenanker wieder her.
    def read(self, lines: list[str], prompt_text: str) -> str:
        self.render(lines, prompt_text)
        value = input("")
        self.renderer.reanchor_prompt_line()
        return value

    # Loescht Panel und Prompt-Zeile kontrolliert, damit keine UI-Reste in den Live-Betrieb uebergehen.
    def clear(self) -> None:
        self.render([""] * self.rows, "")

    # Beendet die Session mit einem sauberen Reset des reservierten Bereichs.
    def __exit__(self, exc_type, exc, tb) -> None:
        if self.active:
            self.clear()
            self.active = False
