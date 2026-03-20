from shellrpg_client.commands.registry import visible_commands
from shellrpg_client.render.fallbacks import MediaMode, choose_media_mode

def test_visible_commands_include_walk() -> None:
    names = [command.name for command in visible_commands()]
    assert "walk <richtung>" in names

def test_fallback_selection_prefers_ansi_when_available() -> None:
    assert choose_media_mode(True, True, False, 80) == MediaMode.ANSI
