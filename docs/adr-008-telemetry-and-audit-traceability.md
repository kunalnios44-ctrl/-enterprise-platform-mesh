# ADR-008: Guardrail Auditability and Telemetry Traceability

## Context
When automated checks block a deployment or flag a health issue, teams need clear context on which rule triggered, why it triggered, and whether the failure came from policy or input errors.

## Decision
1. Emit structured, human-readable status and violation messages to standard error/output alongside standardized exit codes (`0`, `1`, `2`).
2. Keep validation logic self-contained and reproducible across local runs and CI pipelines.
3. Document architectural trade-offs and operational expectations in version-controlled ADRs and runbooks.

## Consequences
- Debugging failed checks takes less time because exact failure reasons are surfaced immediately.
- Historical decisions remain clear and reviewable inside the repository.
