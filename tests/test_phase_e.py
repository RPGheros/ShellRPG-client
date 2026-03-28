from pathlib import Path

from shellrpg_client.app import is_game_command, run_shell_command


def test_game_command_detection_accepts_rpg_verbs() -> None:
    assert is_game_command("city build trade hall") is True
    assert is_game_command("auto battle on balanced") is True


def test_game_command_detection_rejects_shell_commands() -> None:
    assert is_game_command("dir") is False
    assert is_game_command("Get-ChildItem") is False


def test_run_shell_command_pwd_returns_current_directory() -> None:
    cwd = Path.cwd()
    next_cwd, output = run_shell_command("pwd", cwd)
    assert next_cwd == cwd
    assert output == str(cwd)
