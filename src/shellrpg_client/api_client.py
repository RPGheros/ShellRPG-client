# ShellRPG Datei-Banner | Client-API | Deutsch kommentiert
from __future__ import annotations

import json
import secrets
from http.client import RemoteDisconnected
from urllib import request
from urllib.error import HTTPError, URLError


class ApiClient:
    # Kapselt alle HTTP-Aufrufe des Terminal-Clients an den lokalen oder entfernten ShellRPG-Server.
    def __init__(self, base_url: str = "http://127.0.0.1:8765", character_name: str = "Ander") -> None:
        self.base_url = base_url.rstrip("/")
        self.character_name = character_name
        self.session_token = ""
        self.login()

    # Baut die Standard-Header für alle API-Anfragen inklusive Sitzungstoken.
    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.session_token:
            headers["X-Session-Token"] = self.session_token
        return headers

    # Meldet den Client am Server an und speichert das ausgehandelte Sitzungstoken lokal.
    def login(self) -> None:
        payload = json.dumps({"character_name": self.character_name, "client_nonce": secrets.token_hex(8), "rejoin": True}).encode("utf-8")
        req = request.Request(f"{self.base_url}/api/login", data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with request.urlopen(req) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (URLError, HTTPError, RemoteDisconnected, ConnectionError) as exc:
            raise ConnectionError(f"Login zum ShellRPG-Server fehlgeschlagen: {exc}") from exc
        self.session_token = data.get("session_token", "")

    # Führt eine HTTP-Anfrage aus und versucht bei Sitzungsproblemen genau einen Rejoin.
    def _request(self, path: str, method: str = "GET", payload: dict | None = None) -> dict:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        req = request.Request(f"{self.base_url}{path}", data=data, headers=self._headers(), method=method)
        try:
            with request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as first_error:
            self.login()
            req = request.Request(f"{self.base_url}{path}", data=data, headers=self._headers(), method=method)
            try:
                with request.urlopen(req) as response:
                    return json.loads(response.read().decode("utf-8"))
            except Exception as second_error:
                raise ConnectionError(f"ShellRPG-Server antwortet nicht stabil: {second_error}") from second_error

    # Führt eine lesende GET-Anfrage aus.
    def get(self, path: str) -> dict:
        return self._request(path, "GET")

    # Holt den aktuellen öffentlichen Spielzustand.
    def state(self) -> dict:
        return self.get("/api/state")

    # Sendet ein Spielkommando an den Server und liefert den neuen Zustands-Snapshot zurück.
    def post_command(self, command: str) -> dict:
        return self._request("/api/command", "POST", {"command": command})

    # Fordert einen Live-Recovery-Versuch auf dem Server an.
    def recover_live(self) -> dict:
        return self._request("/api/recover/live", "POST", {})

    # Sendet die Charaktererstellung an den Server und speichert den neuen Namen lokal im Client.
    def create_character(self, payload: dict) -> dict:
        result = self._request("/api/character/create", "POST", payload)
        if result.get("ok") and payload.get("character_name"):
            self.character_name = str(payload["character_name"])
            self.login()
        return result

    # Fordert einen sicheren Savepoint an, ohne den Server zum sofortigen Speichern zu zwingen.
    def request_safe_save(self) -> dict:
        return self._request("/api/save/request", "POST", {})
