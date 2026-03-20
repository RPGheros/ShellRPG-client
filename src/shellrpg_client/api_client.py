from __future__ import annotations

import json
from urllib import request


class ApiClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8765") -> None:
        self.base_url = base_url.rstrip("/")

    def get(self, path: str) -> dict:
        with request.urlopen(f"{self.base_url}{path}") as response:
            return json.loads(response.read().decode("utf-8"))

    def post_command(self, command: str) -> dict:
        payload = json.dumps({"command": command}).encode("utf-8")
        req = request.Request(
            f"{self.base_url}/api/command",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
