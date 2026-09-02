from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import httpx

from wfeval_sandbox.settings import UiPathSettings


@dataclass
class AccessToken:
    value: str
    expires_at: float

    def is_valid(self, now: float, leeway_s: int = 60) -> bool:
        return now + leeway_s < self.expires_at


class UiPathAuthError(RuntimeError):
    """Raised when the sandbox cannot obtain a UiPath access token."""


class UiPathTokenProvider:
    def __init__(self, settings: UiPathSettings, client: httpx.Client | None = None) -> None:
        self._settings = settings
        self._client = client or httpx.Client(timeout=10)
        self._cached_token: AccessToken | None = None

    def get_token(self) -> str:
        now = time.time()
        if self._cached_token and self._cached_token.is_valid(now):
            return self._cached_token.value

        token = self._request_token(now)
        self._cached_token = token
        return token.value

    def _request_token(self, now: float) -> AccessToken:
        missing = self._settings.missing_live_fields()
        if missing:
            raise UiPathAuthError(f"Missing UiPath OAuth settings: {', '.join(missing)}")

        response = self._client.post(
            self._settings.token_url or "",
            data={
                "grant_type": "client_credentials",
                "client_id": self._settings.client_id,
                "client_secret": self._settings.client_secret,
                "scope": self._settings.scope,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise UiPathAuthError(f"UiPath token request failed: {exc.response.status_code}") from exc

        payload: dict[str, Any] = response.json()
        access_token = payload.get("access_token")
        if not isinstance(access_token, str) or not access_token:
            raise UiPathAuthError("UiPath token response did not include access_token")

        expires_in = int(payload.get("expires_in", 3600))
        return AccessToken(value=access_token, expires_at=now + expires_in)

