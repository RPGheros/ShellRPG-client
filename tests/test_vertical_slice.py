from pathlib import Path

from shellrpg_client.api_client import ApiClient
from shellrpg_client.app import resolve_character_selection, run_shell_command


def test_api_headers_include_session_token_when_present() -> None:
    client = object.__new__(ApiClient)
    client.session_token = "token-123"
    assert client._headers()["X-Session-Token"] == "token-123"


def test_login_payload_prefers_account_identity_when_available() -> None:
    client = object.__new__(ApiClient)
    client.character_name = "Neowulf"
    client.player_account_id = "acct-123"
    client.device_id = "device-123"
    payload = client._login_payload()
    assert payload["player_account_id"] == "acct-123"
    assert payload["device_id"] == "device-123"
    assert payload["auth_provider"] == "local-device"


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


def test_resolve_character_selection_accepts_index_name_and_id() -> None:
    entries = [
        {"character_id": "char-a", "character_name": "Lyra"},
        {"character_id": "char-b", "character_name": "Korin"},
    ]
    assert resolve_character_selection("2", entries)["character_id"] == "char-b"
    assert resolve_character_selection("Lyra", entries)["character_id"] == "char-a"
    assert resolve_character_selection("char-b", entries)["character_name"] == "Korin"


def test_api_client_matrix_health_uses_health_path() -> None:
    client = object.__new__(ApiClient)
    seen: list[str] = []

    def fake_get(path: str) -> dict:
        seen.append(path)
        return {"ok": True, "path": path}

    client.get = fake_get  # type: ignore[assignment]
    result = client.matrix_health()

    assert result["path"] == "/api/matrix/health"
    assert seen == ["/api/matrix/health"]


def test_api_client_matrix_status_uses_status_path() -> None:
    client = object.__new__(ApiClient)
    seen: list[str] = []

    def fake_get(path: str) -> dict:
        seen.append(path)
        return {"ok": True, "path": path}

    client.get = fake_get  # type: ignore[assignment]
    result = client.matrix_status()

    assert result["path"] == "/api/matrix/status"
    assert seen == ["/api/matrix/status"]
