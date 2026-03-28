from pathlib import Path

from shellrpg_client.api_client import ApiClient
from shellrpg_client.app import run_shell_command


def test_api_headers_include_session_token_when_present() -> None:
    client = object.__new__(ApiClient)
    client.session_token = "token-123"
    assert client._headers()["X-Session-Token"] == "token-123"


def test_run_shell_command_changes_directory_locally() -> None:
    cwd = Path.cwd()
    next_cwd, output = run_shell_command("cd ..", cwd)
    assert next_cwd == cwd.parent.resolve()
    assert output == str(cwd.parent.resolve())


def test_run_shell_command_reports_missing_directory() -> None:
    cwd = Path.cwd()
    next_cwd, output = run_shell_command("cd does-not-exist-shellrpg", cwd)
    assert next_cwd == cwd
    assert "Pfad nicht gefunden" in output
