from __future__ import annotations

from fastapi.testclient import TestClient

from wfeval_sandbox.main import app


client = TestClient(app)


def test_deploy_rejects_empty_artifact_with_platform_diagnostic() -> None:
    response = client.post(
        "/v1/deploy",
        json={"platform": "uipath_maestro", "artifact": {"format": "bpmn_xml", "content": ""}},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["accepted"] is False
    assert body["diagnostics"][0]["code"] == "PLT-DEPLOY-REJECTED"


def test_execution_stub_returns_schema_valid_trace_with_actuals() -> None:
    create_response = client.post(
        "/v1/executions",
        json={
            "artifact": {"format": "bpmn_xml", "content": "<definitions />"},
            "test_cases": [
                {
                    "case_id": "tc_003",
                    "kind": "boundary",
                    "input": {"amount": 10000},
                    "assertions": [
                        {
                            "type": "path",
                            "must_traverse": ["Start", "Gateway_amount", "Task_approval"],
                        }
                    ],
                }
            ],
            "mocks": [],
            "timeout_s": 900,
        },
    )

    assert create_response.status_code == 202
    poll_response = client.get(create_response.json()["poll_url"])

    assert poll_response.status_code == 200
    report = poll_response.json()
    assert report["status"] == "complete"
    assert report["results"][0]["actual_path"] == ["Start", "Gateway_amount", "Task_approval"]
    assert report["traces"][0]["actuals"]["llm_input_tokens"] == 0

