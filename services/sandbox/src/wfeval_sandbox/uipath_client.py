from __future__ import annotations

import httpx

from wfeval_sandbox.auth import UiPathTokenProvider
from wfeval_sandbox.settings import UiPathSettings


class UiPathClient:
    def __init__(
        self,
        settings: UiPathSettings,
        token_provider: UiPathTokenProvider,
        client: httpx.Client | None = None,
    ) -> None:
        self._settings = settings
        self._token_provider = token_provider
        self._client = client or httpx.Client(timeout=30)

    def health_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token_provider.get_token()}",
            "X-UIPATH-OrganizationUnitId": self._settings.folder_id or "",
        }

