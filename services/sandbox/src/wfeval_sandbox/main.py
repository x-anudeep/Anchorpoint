from __future__ import annotations

from fastapi import FastAPI, HTTPException, status

from wfeval.core import Diagnostic
from wfeval.core.diagnostics import Severity
from wfeval_sandbox.models import (
    AssetRegistry,
    DeployRequest,
    DeployResponse,
    ExecutionAccepted,
    ExecutionReport,
    ExecutionRequest,
)
from wfeval_sandbox.repository import InMemoryExecutionRepository
from wfeval_sandbox.settings import SandboxMode, UiPathSettings

app = FastAPI(title="Workflow Eval Sandbox Execution", version="0.1.0")
repository = InMemoryExecutionRepository()
settings = UiPathSettings.from_env()


@app.post("/v1/deploy", response_model=DeployResponse)
def deploy(request: DeployRequest) -> DeployResponse:
    if settings.mode == SandboxMode.DISABLED:
        return DeployResponse(
            accepted=False,
            diagnostics=[
                Diagnostic(
                    code="PLT-DEPLOY-REJECTED",
                    severity=Severity.ERROR,
                    message="Sandbox deployment is disabled in this environment.",
                    suggested_fix="Enable stub or live sandbox mode before requesting deployment.",
                )
            ],
        )
    if settings.mode == SandboxMode.LIVE and settings.missing_live_fields():
        return DeployResponse(
            accepted=False,
            diagnostics=[
                Diagnostic(
                    code="PLT-DEPLOY-REJECTED",
                    severity=Severity.ERROR,
                    message="Live UiPath deployment is missing required configuration.",
                    suggested_fix="Set UiPath OAuth and folder environment variables for Sandbox.",
                )
            ],
        )
    if not request.artifact.content.strip():
        return DeployResponse(
            accepted=False,
            diagnostics=[
                Diagnostic(
                    code="PLT-DEPLOY-REJECTED",
                    severity=Severity.ERROR,
                    message="Artifact content is empty.",
                    suggested_fix="Submit a non-empty BPMN artifact before deployment.",
                )
            ],
        )
    return DeployResponse(accepted=True)


@app.post("/v1/executions", response_model=ExecutionAccepted, status_code=status.HTTP_202_ACCEPTED)
def create_execution(request: ExecutionRequest) -> ExecutionAccepted:
    execution_id = repository.create_stub_execution(request)
    return ExecutionAccepted(execution_id=execution_id, poll_url=f"/v1/executions/{execution_id}")


@app.get("/v1/executions/{execution_id}", response_model=ExecutionReport)
def get_execution(execution_id: str) -> ExecutionReport:
    report = repository.get_execution(execution_id)
    if report is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="execution not found")
    return report


@app.get("/v1/assets", response_model=AssetRegistry)
def get_assets() -> AssetRegistry:
    return repository.get_assets()
