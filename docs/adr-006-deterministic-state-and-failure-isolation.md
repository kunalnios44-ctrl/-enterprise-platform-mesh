# ADR-006: Failure Isolation and Deterministic State Boundaries

## Context
In distributed platform and CI/CD systems, a fault in one component or an invalid input payload can cascade into broader outages or ambiguous pipeline states if boundaries are not isolated.

## Decision
1. Isolate each guardrail plane (`security`, `dr-backup`, `infra`, `observability`, `platform`, and `platform-guardrail`) with explicit validation boundaries and deterministic exit codes (`0`, `1`, `2`).
2. Reject malformed or oversized (`> 1 MiB`) inputs immediately before downstream evaluation so invalid data cannot corrupt state.
3. Keep automated checks self-contained and repeatable so every change is verified against the same baseline.

## Consequences
- Faults remain contained within clear boundaries instead of cascading across workflows or environments.
- System behavior stays predictable under stress, bad payloads, and high-frequency changes.
- 
