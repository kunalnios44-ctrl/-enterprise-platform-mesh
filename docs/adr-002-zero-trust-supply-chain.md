# ADR-002: Zero-Trust Supply Chain and Immutable Container Delivery

## Context
Deploying unverified code, over-privileged credentials, or mutable container tags into Kubernetes clusters introduces severe security and blast-radius risks across multi-cloud environments.

## Decision
1. Enforce keyless authentication via OIDC and least-privilege IAM/RBAC policies instead of long-lived static secrets.
2. Run static analysis (`Semgrep`), vulnerability scanning (`Trivy`), and cryptographic image signing (`Cosign`) prior to deployment.
3. Pin container deployments by immutable digest (`@sha256:...`) rather than mutable tags (`:latest`).

## Consequences
- Unsigned or vulnerable artifacts are blocked before reaching GitOps rollout.
- Teams must maintain clean OIDC trust configurations and digest-pinned manifests in their delivery workflows.
- 
