from __future__ import annotations

import httpx
import pytest

from wfeval_sandbox.auth import UiPathAuthError, UiPathTokenProvider
from wfeval_sandbox.settings import SandboxMode, UiPathSettings


def test_missing_live_settings_raise_clear_auth_error() -> None:
    provider = UiPathTokenProvider(UiPathSettings(mode=SandboxMode.LIVE))

    with pytest.raises(UiPathAuthError, match="UIPATH_TOKEN_URL"):
        provider.get_token()


def test_token_provider_uses_client_credentials_and_caches_token() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"access_token": "tok_123", "expires_in": 3600})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    provider = UiPathTokenProvider(
        UiPathSettings(
            mode=SandboxMode.LIVE,
            token_url="https://cloud.uipath.example/connect/token",
            client_id="client-id",
            client_secret="client-secret",
            scope="OR.Jobs OR.Folders",
            base_url="https://cloud.uipath.example/orchestrator",
            folder_id="folder-1",
        ),
        client=client,
    )

    assert provider.get_token() == "tok_123"
    assert provider.get_token() == "tok_123"
    assert len(calls) == 1
    assert "grant_type=client_credentials" in calls[0].content.decode()

