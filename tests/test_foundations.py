from shellrpg_client.app import build_demo_screen
from shellrpg_client.render.fallbacks import MediaMode, choose_media_mode

def test_demo_screen_contains_versionless_foundation_shape() -> None:
    screen = build_demo_screen()
    assert "Graufurt-Osttor" in screen

def test_fallback_selection_prefers_ansi_when_available() -> None:
    assert choose_media_mode(True, True, False, 80) == MediaMode.ANSI
