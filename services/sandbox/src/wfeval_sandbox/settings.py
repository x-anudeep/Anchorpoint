from __future__ import annotations

import os
from dataclasses import dataclass
from enum import StrEnum


class SandboxMode(StrEnum):
    STUB = "stub"
    LIVE = "live"
    DISABLED = "disabled"


@dataclass(frozen=True)
class UiPathSettings:
    mode: SandboxMode = SandboxMode.STUB
    token_url: str | None = None
    client_id: str | None = None
    client_secret: str | None = None
    scope: str | None = None
    base_url: str | None = None
    folder_id: str | None = None

    @classmethod
    def from_env(cls) -> "UiPathSettings":
        mode = SandboxMode(os.getenv("SANDBOX_MODE", SandboxMode.STUB))
        return cls(
            mode=mode,
            token_url=os.getenv("UIPATH_TOKEN_URL"),
            client_id=os.getenv("UIPATH_CLIENT_ID"),
            client_secret=os.getenv("UIPATH_CLIENT_SECRET"),
            scope=os.getenv("UIPATH_SCOPE"),
            base_url=os.getenv("UIPATH_BASE_URL"),
            folder_id=os.getenv("UIPATH_FOLDER_ID"),
        )

    def missing_live_fields(self) -> list[str]:
        required = {
            "UIPATH_TOKEN_URL": self.token_url,
            "UIPATH_CLIENT_ID": self.client_id,
            "UIPATH_CLIENT_SECRET": self.client_secret,
            "UIPATH_BASE_URL": self.base_url,
            "UIPATH_FOLDER_ID": self.folder_id,
        }
        return [name for name, value in required.items() if not value]

