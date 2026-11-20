# ADR-009: Secretless Authentication and Least-Privilege Access Boundaries

## Context
Long-lived static credentials and overly broad permissions increase blast radius if a credential is leaked or a pipeline step is misconfigured.

## Decision
1. Prefer short-lived, federated identity/OIDC authentication where supported instead of static long-lived secrets.
2. Scope service accounts, roles, and permissions strictly to the minimum actions and resources required for each guardrail or workflow step.
3. Fail closed when required configuration or credentials are missing or invalid.

## Consequences
- Credential exposure risk and privilege blast radius are reduced across automation and environments.
- Workflows remain explicit about required permissions and fail cleanly on misconfiguration.
