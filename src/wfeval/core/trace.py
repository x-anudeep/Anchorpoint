from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Actuals(BaseModel):
    llm_input_tokens: int = Field(default=0, ge=0)
    llm_output_tokens: int = Field(default=0, ge=0)
    agent_turns: int = Field(default=0, ge=0)
    duration_ms: int = Field(default=0, ge=0)
    robot_units: float = Field(default=0.0, ge=0)


class ElementEvent(BaseModel):
    element_id: str
    status: Literal["started", "completed", "failed", "skipped"]
    timestamp_ms: int | None = Field(default=None, ge=0)
    duration_ms: int | None = Field(default=None, ge=0)
    outcome: str | None = None


class Trace(BaseModel):
    case_id: str
    elements: list[str] = Field(default_factory=list)
    events: list[ElementEvent] = Field(default_factory=list)
    actuals: Actuals = Field(default_factory=Actuals)
    final_variables: dict[str, Any] = Field(default_factory=dict)

