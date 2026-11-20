# ADR 0001: Path-Isolated CI/CD and Zero-Trust Multi-Cloud Baseline

- **Status:** Accepted
- **Date:** 2026-11-20

## Context
Managing multi-cloud infrastructure (AWS, Azure, GCP), Kubernetes clusters (EKS, AKS, GKE), observability, security policies, and disaster recovery in a single repository can create noisy CI runs and inconsistent security enforcement.

## Decision
1. Isolate GitHub Actions workflows with strict `paths:` filters so unrelated commits do not trigger unnecessary pipeline runs.
2. Enforce OIDC short-lived identity federation instead of static cloud credentials across environments (`dev`, `staging`, `prod`).
3. Pair declarative configurations with lightweight verification scripts and admission guardrails.

## Consequences
- Faster, predictable CI/CD feedback with zero unnecessary pipeline noise.
- Consistent environment promotion and auditable security boundaries across all layers.
