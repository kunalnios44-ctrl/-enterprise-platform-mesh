# ADR-010: Immutable Artifacts and Reproducible Verification

## Context
Unpinned dependencies or mutable build outputs can cause inconsistent behavior between local checks, CI verification runs, and packaged artifacts.

## Decision
1. Pin verification scripts and tests to deterministic inputs, explicit schemas, and consistent exit codes (`0`, `1`, `2`).
2. Produce CI artifacts only after passing verification checks so packaged outputs reflect verified repository state.
3. Avoid hidden mutable runtime side effects during guardrail evaluation.

## Consequences
- Verification results remain repeatable across runs and environments.
- Packaged artifacts align cleanly with verified source and configuration state.
