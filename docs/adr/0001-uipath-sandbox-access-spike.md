# ADR 0001: UiPath Sandbox Access Spike

## Status

Accepted for the P3 day-1 spike.

## Context

The Sandbox Execution service is the only workflow-eval service that touches
UiPath credentials. The project plan makes sandbox tenant access a day-2 gate
because L5 acceptance and L6 execution cannot be validated without it.

## Decision

P3 will isolate all UiPath calls behind a small client boundary and keep the HTTP
service contract live even when credentials are absent. The service will support
three execution modes:

- `live`: deploys and executes against the configured UiPath sandbox folder;
- `stub`: returns schema-valid responses for integration and contract testing;
- `disabled`: rejects live-only operations with `PLT-DEPLOY-REJECTED` diagnostics.

OAuth2 client-credentials configuration is read from environment variables:

- `UIPATH_TOKEN_URL`
- `UIPATH_CLIENT_ID`
- `UIPATH_CLIENT_SECRET`
- `UIPATH_SCOPE`
- `UIPATH_BASE_URL`
- `UIPATH_FOLDER_ID`

No other service receives these values.

## Consequences

The gateway can integrate with Sandbox on day 3 using stub responses, while live
tenant access remains a visible operational gate. If sandbox access is still
blocked by day 3, P3 pivots L6 behavior to a local engine while preserving the
same `/v1/executions` contract and canonical trace shape.

