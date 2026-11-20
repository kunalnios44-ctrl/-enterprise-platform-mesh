# ADR-003: Deterministic DR Recovery Gates and SLO Burn-Rate Controls

## Context
Unverified backups or uncontrolled service degradation can turn minor incidents into prolonged outages across production clusters.

## Decision
1. Require backup age (`rpo_age_minutes`) to stay within the target RPO window and require recent restore verification (`restore_verified == true`) before treating backups as healthy.
2. Enforce SLO checks on availability, `p99` latency, and error-budget burn rate so high-burn rollouts are flagged early.
3. Keep all guardrail scripts deterministic with bounded input (`1 MiB`) and standardized exit codes (`0`, `1`, `2`).

## Consequences
- Teams get objective pass/fail signals before promotion or recovery actions.
- Operators spend less time guessing and more time acting on verified state.
