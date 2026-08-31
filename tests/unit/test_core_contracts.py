from __future__ import annotations

import pytest
from pydantic import ValidationError

from wfeval.core import Actuals, Assertion, AssertionType, MockDefinition, TestCase, TestCaseKind


def test_actuals_defaults_match_cost_calibration_shape() -> None:
    actuals = Actuals()

    assert actuals.model_dump() == {
        "llm_input_tokens": 0,
        "llm_output_tokens": 0,
        "agent_turns": 0,
        "duration_ms": 0,
        "robot_units": 0.0,
    }


def test_path_assertions_require_a_path() -> None:
    with pytest.raises(ValidationError, match="must_traverse"):
        Assertion(type=AssertionType.PATH)


def test_testcase_accepts_prompt_derived_assertions_and_mocks() -> None:
    case = TestCase(
        case_id="tc_003",
        kind=TestCaseKind.BOUNDARY,
        input={"amount": 10000},
        assertions=[
            Assertion(
                type=AssertionType.PATH,
                must_traverse=["Start", "Gateway_amount", "Task_approval"],
            )
        ],
    )
    mock = MockDefinition(host="api.payments.internal", path="/charge", response={"ok": True})

    assert case.case_id == "tc_003"
    assert mock.status == 200
