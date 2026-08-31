from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class TestCaseKind(StrEnum):
    __test__ = False

    HAPPY = "happy"
    BOUNDARY = "boundary"
    ADVERSARIAL = "adversarial"


class AssertionType(StrEnum):
    PATH = "path"
    OUTPUT = "output"
    INVARIANT = "invariant"


class Assertion(BaseModel):
    type: AssertionType
    must_traverse: list[str] | None = None
    field: str | None = None
    equals: Any | None = None
    expr: str | None = None

    @model_validator(mode="after")
    def require_shape_for_type(self) -> "Assertion":
        if self.type == AssertionType.PATH and not self.must_traverse:
            raise ValueError("path assertions require must_traverse")
        if self.type == AssertionType.OUTPUT and self.field is None:
            raise ValueError("output assertions require field")
        if self.type == AssertionType.INVARIANT and self.expr is None:
            raise ValueError("invariant assertions require expr")
        return self


class MockDefinition(BaseModel):
    host: str
    path: str = Field(pattern=r"^/")
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "POST"
    status: int = Field(default=200, ge=100, le=599)
    response: dict[str, Any] = Field(default_factory=dict)
    headers: dict[str, str] = Field(default_factory=dict)


class TestCase(BaseModel):
    __test__ = False

    case_id: str = Field(pattern=r"^[A-Za-z0-9_.:-]+$")
    kind: TestCaseKind
    input: dict[str, Any] = Field(default_factory=dict)
    assertions: list[Assertion] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
