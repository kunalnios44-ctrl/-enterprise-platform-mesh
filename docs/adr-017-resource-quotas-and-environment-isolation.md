# ADR-017: Environment Isolation and Explicit Resource Bounds

## Context
Shared tooling and multi-environment pipelines can experience cross-environment mistakes or uncontrolled resource usage if boundaries and limits are not stated explicitly.

## Decision
1. Keep environment context and validation rules explicit in guardrail inputs and rollout checks rather than relying on implicit defaults.
2. Enforce strict payload size limits (`1 MiB`) and clear bounds on thresholds such as replicas, canary traffic, and RPO age.
3. Fail closed when required environment or configuration fields are missing or invalid.

## Consequences
- Cross-environment misconfigurations are caught earlier in automation.
- Resource limits remain clear, auditable, and consistent across checks.
