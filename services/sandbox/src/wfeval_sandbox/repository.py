from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from wfeval.core import Actuals, ElementEvent, Trace
from wfeval_sandbox.models import (
    Asset,
    AssetRegistry,
    CaseResult,
    ExecutionReport,
    ExecutionRequest,
    ExecutionStatus,
)


@dataclass
class InMemoryExecutionRepository:
    executions: dict[str, ExecutionReport] = field(default_factory=dict)
    assets: list[Asset] = field(default_factory=list)

    def create_stub_execution(self, request: ExecutionRequest) -> str:
        execution_id = f"ex_{uuid4().hex[:16]}"
        results: list[CaseResult] = []
        traces: list[Trace] = []

        for test_case in request.test_cases:
            expected_path = _expected_path(test_case)
            results.append(
                CaseResult(
                    case_id=test_case.case_id,
                    status="pass",
                    expected_path=expected_path,
                    actual_path=expected_path,
                )
            )
            traces.append(
                Trace(
                    case_id=test_case.case_id,
                    elements=expected_path,
                    events=[
                        ElementEvent(element_id=element_id, status="completed")
                        for element_id in expected_path
                    ],
                    actuals=Actuals(duration_ms=0),
                    final_variables={"stubbed": True},
                )
            )

        self.executions[execution_id] = ExecutionReport(
            status=ExecutionStatus.COMPLETE,
            results=results,
            traces=traces,
        )
        return execution_id

    def get_execution(self, execution_id: str) -> ExecutionReport | None:
        return self.executions.get(execution_id)

    def get_assets(self) -> AssetRegistry:
        return AssetRegistry(assets=self.assets)


def _expected_path(test_case) -> list[str]:
    for assertion in test_case.assertions:
        if assertion.must_traverse:
            return assertion.must_traverse
    return ["Start", "End"]

