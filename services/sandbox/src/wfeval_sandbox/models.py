from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from wfeval.core import Diagnostic, MockDefinition, TestCase, Trace


class Platform(StrEnum):
    UIPATH_MAESTRO = "uipath_maestro"


class Artifact(BaseModel):
    format: str = Field(pattern=r"^[a-z0-9_]+$")
    content: str
    name: str | None = None


class DeployRequest(BaseModel):
    platform: Platform
    artifact: Artifact


class DeployResponse(BaseModel):
    accepted: bool
    diagnostics: list[Diagnostic] = Field(default_factory=list)


class ExecutionRequest(BaseModel):
    artifact: Artifact
    test_cases: list[TestCase]
    mocks: list[MockDefinition] = Field(default_factory=list)
    timeout_s: int = Field(default=900, ge=1, le=3600)
    callback_url: str | None = None


class ExecutionAccepted(BaseModel):
    execution_id: str
    poll_url: str


class ExecutionStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CaseResult(BaseModel):
    case_id: str
    status: str
    expected_path: list[str] = Field(default_factory=list)
    actual_path: list[str] = Field(default_factory=list)
    failed_assertion: str | None = None


class ExecutionReport(BaseModel):
    status: ExecutionStatus
    results: list[CaseResult] = Field(default_factory=list)
    traces: list[Trace] = Field(default_factory=list)
    diagnostics: list[Diagnostic] = Field(default_factory=list)


class Asset(BaseModel):
    asset_id: str
    name: str
    kind: str
    platform: Platform = Platform.UIPATH_MAESTRO
    metadata: dict[str, Any] = Field(default_factory=dict)


class AssetRegistry(BaseModel):
    assets: list[Asset] = Field(default_factory=list)
    source: str = "stub"

