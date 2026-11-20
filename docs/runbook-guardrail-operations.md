# Guardrail Operations Runbook

## Exit Code Triage
- **Exit `0` (Pass / Healthy)**: Guardrail checks passed; normal CI/CD or release flow continues.
- **Exit `1` (Policy / Guardrail Violation)**: Action blocked by rule (e.g., RPO breach, blast-radius limit, SLO burn rate, or rollout constraint). Review stderr violation message and fix configuration or policy input before retrying.
- **Exit `2` (Payload / Runtime / I/O Error)**: Input was empty, malformed JSON, exceeded `1 MiB`, or had invalid field types/values. Fix upstream payload generation or input schema.
