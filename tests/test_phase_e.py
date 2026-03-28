from pathlib import Path

from shellrpg_client.api_client import ApiClient
from shellrpg_client.app import (
    control_write_allowed,
    is_character_command,
    is_control_command,
    is_game_command,
    is_observer_safe_game_command,
    run_shell_command,
)


def test_game_command_detection_accepts_rpg_verbs() -> None:
    assert is_game_command("city build trade hall") is True
    assert is_game_command("auto battle on balanced") is True
    assert is_game_command("merchant help") is True
    assert is_game_command("cube help") is True


def test_game_command_detection_rejects_shell_commands() -> None:
    assert is_game_command("dir") is False
    assert is_game_command("Get-ChildItem") is False


def test_character_command_detection_accepts_tree_commands() -> None:
    assert is_character_command("character list") is True
    assert is_character_command("char use 2") is True
    assert is_character_command("dir") is False


def test_control_command_detection_accepts_role_commands() -> None:
    assert is_control_command("control status") is True
    assert is_control_command("controller take") is True
    assert is_control_command("git status") is False


def test_observer_safe_game_command_allows_read_only_catalog_paths() -> None:
    snapshot = {
        "status": {"control_mode": "controller-observer", "control_write_allowed": False},
        "command_details": [
            {"usage": "look", "aliases": ["look"], "observer_safe": True},
            {"usage": "walk north|south|west|east|x,y", "aliases": ["walk"], "observer_safe": False},
        ],
    }
    assert is_observer_safe_game_command(snapshot, "look") is True
    assert is_observer_safe_game_command(snapshot, "walk north") is False


def test_control_write_allowed_reads_status_flag() -> None:
    assert control_write_allowed({"status": {"control_mode": "controller-observer", "control_write_allowed": True}}) is True
    assert control_write_allowed({"status": {"control_mode": "controller-observer", "control_write_allowed": False}}) is False


def test_api_client_remembers_live_event_cursor_from_snapshot_payload() -> None:
    client = ApiClient.__new__(ApiClient)
    client.last_live_event_id = 0
    client.last_live_event_reason = ""

    client._remember_live_event({"status": {"live_event_id": 7, "live_event_reason": "control-takeover"}})

    assert client.last_live_event_id == 7
    assert client.last_live_event_reason == "control-takeover"


def test_run_shell_command_pwd_returns_current_directory() -> None:
    cwd = Path.cwd()
    next_cwd, output = run_shell_command("pwd", cwd)
    assert next_cwd == cwd
    assert output == str(cwd)
