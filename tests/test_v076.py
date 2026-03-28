# ShellRPG Datei-Banner | Client-Tests v0.7.6 | Deutsch kommentiert
from shellrpg_client.app import is_game_command, moon_scale, venus_scale


# Prüft, dass typische Spielbefehle als Spielkommandos erkannt werden.
def test_game_command_detection() -> None:
    assert is_game_command('hunt') is True
    assert is_game_command('npc buy Ander Heiltrunk') is True
    assert is_game_command('dir') is False


# Prüft die kompakten Symbolskalen für Mond und Venus.
def test_phase_scales_are_non_empty() -> None:
    assert moon_scale('Abnehmende Sichel')
    assert venus_scale('Dämmerung')
