from __future__ import annotations

import io
from pathlib import Path

from shellrpg_client.app import (
    HEADER_ROWS,
    LiveContext,
    SCROLL_PANEL_ROWS,
    build_intro_panel_lines,
    build_scroll_panel_lines,
    compact_status_lines,
    render_live_prompt,
    run_shell_command,
)
from shellrpg_client.terminal_layout import (
    ReservedTerminalRenderer,
    format_shell_prompt,
    strip_ansi,
)


def make_snapshot() -> dict:
    return {
        "status": {
            "character_name": "Wuffie",
            "class_name": "Ritter",
            "race_name": "Nekari",
            "level": 5,
            "location_label": "Graufurt-Osttor mit einem unnoetig langen Namen fuer schmale Konsolen",
            "coords_label": "2048,2048",
            "hp_current": 52,
            "hp_max": 104,
            "mana_current": 52,
            "mana_max": 52,
            "gold": 2,
            "silver": 137,
            "hunger": "spuerbar",
            "weather_label": "Klarer Himmel ueber einem sehr breiten Horizont",
            "time_label": "Abend · 17:43 Europe/Berlin",
            "moon_label": "Neumond",
            "venus_label": "Morgenstern",
            "active_action": "combat",
            "auto_battle_enabled": False,
            "overlay_message": "Der Ritter prueft die Umgebung und wartet auf den naechsten Befehl",
            "media_terminal_file": "",
        }
    }


def test_compact_status_lines_stay_within_terminal_width() -> None:
    lines = compact_status_lines(make_snapshot(), spinner_index=2, columns=48)
    assert len(lines) == HEADER_ROWS
    assert all(len(strip_ansi(line)) <= 47 for line in lines)


def test_intro_panel_lines_fit_small_terminal_width() -> None:
    lines = build_intro_panel_lines(
        52,
        "ShellRPG Initiation Bootstrap",
        ["Eine ruhige Phase.", "Noch eine ruhigere Phase."],
        footer="Synchronisiere Renderzustand",
    )
    assert all(len(strip_ansi(line)) <= 51 for line in lines)


def test_scroll_panel_lines_fit_small_terminal_width_and_keep_fixed_height() -> None:
    lines = build_scroll_panel_lines(
        54,
        "Schriftrolle der Herkunft",
        "Die Pergamentrolle bleibt einzeilig und ruhig.",
        ["1. Menschen", "2. Amazonen", "3. Nekari"],
        footer="Waehle eine Zahl und bestaetige mit Enter.",
    )
    assert len(lines) == SCROLL_PANEL_ROWS
    assert all(len(strip_ansi(line)) <= 53 for line in lines)


def test_format_shell_prompt_shortens_long_path_without_wrapping() -> None:
    prompt = format_shell_prompt(Path(r"d:\Projekte\ShellRPG\ShellRPG-client\mit\einem\sehr\langen\pfad"), 42)
    assert len(prompt) <= 41
    assert prompt.endswith("> ")


def test_render_live_prompt_leaves_prompt_as_last_visible_line() -> None:
    stream = io.StringIO()
    renderer = ReservedTerminalRenderer(stream=stream, fallback_columns=60, fallback_lines=20)
    context = LiveContext(snapshot=make_snapshot(), spinner_index=1)
    render_live_prompt(renderer, context, Path(r"d:\Projekte\ShellRPG\ShellRPG-client"))
    plain = strip_ansi(stream.getvalue()).replace("\r", "\n")
    visible_lines = [line for line in plain.splitlines() if line.strip()]
    assert visible_lines[-1].startswith("PS ")
    assert "Aktion:" not in visible_lines[-1]


def test_run_shell_command_passthrough_disables_output_capture(monkeypatch) -> None:
    called: dict[str, object] = {}

    class FakeResult:
        stdout = ""
        stderr = ""
        returncode = 0

    def fake_run(command: str, **kwargs):
        called["command"] = command
        called["kwargs"] = kwargs
        return FakeResult()

    monkeypatch.setattr("shellrpg_client.app.subprocess.run", fake_run)
    next_cwd, output = run_shell_command("git status", Path.cwd(), capture_output=False)
    assert next_cwd == Path.cwd()
    assert output == ""
    assert called["command"] == "git status"
    assert "capture_output" not in called["kwargs"]
