# ADR-005: Multi-Cloud Blast-Radius Controls and Infrastructure Drift Guardrails

## Context
Infrastructure changes across cloud providers can introduce unintended resource deletions, exposed endpoints, or unencrypted storage if applied without automated pre-apply checks.

## Decision
1. Evaluate Terraform plan changes prior to apply and enforce explicit deletion thresholds (`max_deletes`) to bound blast radius.
2. Flag public exposure, disabled encryption, and overly broad ingress on sensitive ports before changes reach production.
3. Pair infrastructure guardrails with deterministic exit codes and automated tests so regressions are caught early.

## Consequences
- High-blast-radius or insecure infrastructure changes are caught before apply.
- Teams maintain a clear audit trail of why specific infrastructure guardrails exist.
- 
