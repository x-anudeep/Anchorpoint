# Workflow Evaluation - P3 Sandbox Execution

This directory contains the P3-owned Sandbox Execution slice for the workflow
validation and evaluation layer. The service owns platform acceptance, execution
jobs, trace capture, and the deployed asset registry used by Validation L2.

The implementation is intentionally contract-first. The first three days focus on:

- confirming UiPath sandbox integration assumptions and fallback strategy;
- freezing the `TestCase`, `MockDefinition`, `Trace`, and `Actuals` shapes shared
  with P2 and P4;
- exposing stubbed but schema-valid Sandbox endpoints; and
- landing the OAuth2 client-credentials foundation for real UiPath calls.

## Local checks

```bash
PYTHONPATH=src:services/sandbox/src pytest
```

