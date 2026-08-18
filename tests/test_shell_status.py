from __future__ import annotations

from shellrpg_client.api_client import ApiClient
from shellrpg_client import shell_status


def test_api_client_uses_text_status_path() -> None:
    client = ApiClient.__new__(ApiClient)
    seen: list[str] = []
    client._request_text = lambda path: seen.append(path) or "one\ntwo\nthree"

    assert client.status_text() == "one\ntwo\nthree"
    assert seen == ["/api/status/text"]


def test_shell_status_command_prints_exactly_three_lines(monkeypatch, capsys) -> None:
    captured: dict[str, str] = {}

    class FakeApiClient:
        def __init__(self, **kwargs) -> None:
            captured.update(kwargs)

        def status_text(self) -> str:
            return " ShellRPG: Roman \n HP 24/24 \n Action: idle "
    monkeypatch.setattr(shell_status, "ApiClient", FakeApiClient)

    result = shell_status.main(
        [
            "--base-url",
            "http://localhost:9999",
            "--character-name",
            "Roman",
            "--account-id",
            "account-1",
        ]
    )

    assert result == 0
    assert capsys.readouterr().out.splitlines() == [
        "ShellRPG: Roman",
        "HP 24/24",
        "Action: idle",
    ]
    assert captured == {
        "base_url": "http://localhost:9999",
        "character_name": "Roman",
        "player_account_id": "account-1",
    }


def test_shell_status_command_is_silent_for_invalid_or_offline_status(monkeypatch, capsys) -> None:
    class OfflineApiClient:
        def __init__(self, **kwargs) -> None:
            raise ConnectionError("offline")

    monkeypatch.setattr(shell_status, "ApiClient", OfflineApiClient)

    assert shell_status.main([]) == 0
    assert capsys.readouterr().out == ""
