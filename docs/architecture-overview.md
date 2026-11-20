# Enterprise Platform Mesh — Architecture Overview

## Core Guardrail Planes
- **Policy & Security (`security/`)**: Validates policy payloads, enforces bounded input (`1 MiB`), and returns deterministic exit codes (`0`, `1`, `2`).
- **DR & Backup Readiness (`dr-backup/`)**: Verifies backup age (`rpo_age_minutes`), RPO limits, and restore verification status before recovery/promotion.
- **Infrastructure Plan (`infra/`)**: Inspects Terraform plan JSON for mass-deletion blast radius (`max_deletes`), public exposure, encryption, and open sensitive ports.
- **Observability & SLO (`observability/`)**: Checks service availability, `p99` latency, and error-budget burn rate before risky releases.
- **Platform Rollout (`platform/` & `platform-guardrail/`)**: Guards Kubernetes rollout parameters and Go guardrail baseline checks alongside CI/CD artifact packaging.
- 
