# ADR-007: Release Promotion Gates and Deterministic Rollback Discipline

## Context
Promoting releases without explicit health checks, SLO signals, or clear rollback boundaries increases the risk of prolonged service degradation during deployments.

## Decision
1. Gate release promotion on passing guardrail verifications, healthy SLO/error-budget signals, and valid rollout constraints.
2. Keep rollout configurations explicit and deterministic so failed promotions halt cleanly without partial or ambiguous states.
3. Require verified recovery/backup readiness and clean test execution prior to packaging release artifacts.

## Consequences
- Unsafe releases are stopped before broader traffic exposure.
- Deployment state remains clear and auditable across environments.
- 
