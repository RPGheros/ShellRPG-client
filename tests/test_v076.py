# ShellRPG Datei-Banner | Client-Tests v0.8.0 | Deutsch kommentiert
from shellrpg_client.app import is_game_command, moon_scale, venus_scale
from shellrpg_client.ui import format_countdown, render_status, status_countdown


# Prüft, dass typische Spielbefehle als Spielkommandos erkannt werden.
def test_game_command_detection() -> None:
    assert is_game_command('hunt') is True
    assert is_game_command('npc buy Ander Heiltrunk') is True
    assert is_game_command('dir') is False


# Prüft die kompakten Symbolskalen für Mond und Venus.
def test_phase_scales_are_non_empty() -> None:
    assert moon_scale('Abnehmende Sichel')
    assert venus_scale('Dämmerung')


def test_status_countdowns_use_seconds_contract() -> None:
    assert format_countdown(239) == "03:59"
    assert format_countdown(20) == "00:20"
    assert format_countdown(60, combat=True) == "00:60"
    assert status_countdown({"reaction_seconds_left": 60}) == "Combat: 00:60"
    assert status_countdown({"activity_type": "gather", "activity_resource_type": "gold", "activity_eta_seconds": 20}) == "Goldzyklus: 00:20"
    assert status_countdown({"active_action": "idle", "idle_reward_eta_seconds": 600}) == "Idle-Drop: 10:00"


def test_render_status_includes_countdown_line() -> None:
    rendered = render_status(
        {
            "character_name": "Mira",
            "class_name": "Ritter",
            "race_name": "Mensch",
            "level": 5,
            "location_label": "Graufurt",
            "coords_label": "2048,2048",
            "hp_current": 50,
            "hp_max": 100,
            "mana_current": 20,
            "mana_max": 40,
            "gold": 1,
            "silver": 2,
            "hunger": "gering",
            "active_action": "walk",
            "activity_type": "walk",
            "activity_eta_seconds": 239,
            "tick_value": 7,
        }
    )

    assert "Countdown Reise: 03:59" in rendered
