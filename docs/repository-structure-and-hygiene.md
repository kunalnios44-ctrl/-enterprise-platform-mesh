# Repository Structure and Hygiene

## Directory Layout
- `.github/workflows/`: Automated CI verification and artifact packaging workflows.
- `docs/`: Architecture decision records (ADRs), architecture overview, runbooks, and hygiene notes.
- `security/`: Policy gate checks and verification tests.
- `dr-backup/`: Disaster recovery and backup readiness checks and tests.
- `infra/`: Infrastructure plan guardrails and verification tests.
- `observability/`: SLO and error-budget guardrails and verification tests.
- `platform/` & `platform-guardrail/`: Rollout guardrails, Go components, and baseline tests.

## Hygiene Standards
- Keep files organized by domain responsibility without stray temporary files.
- Enforce bounded inputs (`1 MiB`), explicit validation, and deterministic exit codes (`0`, `1`, `2`).
- Keep documentation concise, accurate, and aligned with actual repository files.
- 
