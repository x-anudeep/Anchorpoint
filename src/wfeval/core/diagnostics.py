from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class Diagnostic(BaseModel):
    code: str = Field(pattern=r"^[A-Z]+-[A-Z0-9-]+$")
    severity: Severity
    message: str
    element_id: str | None = None
    locator: str | None = None
    suggested_fix: str | None = None

