# ADR-016: Backward Compatibility and Safe Change Evolution

## Context
Breaking payload formats or abrupt contract changes across scripts, pipelines, or environments can cause unexpected failures during incremental rollouts or rollbacks.

## Decision
1. Evolve input schemas and verification contracts incrementally while preserving clear backward compatibility where possible.
2. Reject ambiguous or incompatible inputs explicitly (`exit 2`) rather than silently altering behavior across versions.
3. Update corresponding unit tests and documentation whenever guardrail contracts change.

## Consequences
- Incremental upgrades and rollbacks remain safer and easier to reason about.
- Breaking mismatches are caught explicitly instead of causing silent misbehavior.
