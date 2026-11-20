# ADR-001: Guardrail Exit Codes, Bounded Input, and Strict Schema Validation

## Context
Automated CI/CD pipelines and platform guardrails process configuration, rollout, DR, and policy payloads. Mixing policy failures with malformed input or runtime errors makes automation unreliable and noisy.

## Decision
1. Standardize CLI/script exit codes across guardrails:
   - `0`: Validation passed / healthy state.
   - `1`: Policy, guardrail, RPO, or rollout rule violation detected.
   - `2`: Invalid/malformed input, missing required fields, type mismatch, or runtime/I/O error.
2. Enforce bounded input size (`1 MiB` limit) and strict type checks (including rejecting `bool` where strict integers/numbers are expected).

## Consequences
- CI/CD workflows and operators can distinguish config/policy issues (`1`) from broken payloads or runtime failures (`2`) without guesswork.
- Unbounded payloads or ambiguous types fail fast before reaching downstream environments.
