# ADR-004: CI Verification, Artifact Packaging, and Automated Test Gates

## Context
Guardrail scripts and configuration checks must be verified automatically on commits before packaging release or CI artifacts.

## Decision
1. Run verification and test checks across repository guardrails (`security`, `dr-backup`, `infra`, `observability`, `platform`, and `platform-guardrail`) during CI.
2. Package verified outputs into CI artifacts only after verification steps pass.
3. Keep unit and baseline tests fast, deterministic, and independent of external network calls.

## Consequences
- Broken changes or invalid payloads fail early in CI instead of reaching downstream packaging or deployment stages.
- Contributors get fast feedback loops on every push.
