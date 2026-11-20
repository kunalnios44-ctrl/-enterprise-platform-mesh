# ADR-019: Least-Privilege IAM and RBAC Boundaries

## Context
Over-broad identity permissions or shared service roles increase security exposure and blast radius across cloud accounts, clusters, and automation pipelines.

## Decision
1. Grant only the minimum permissions required for each guardrail check, deployment step, or runtime workload.
2. Separate read/verification roles from mutating or administrative roles across environments.
3. Review and tighten permission boundaries whenever new guardrails or workflows are added.

## Consequences
- Accidental or unauthorized privilege misuse has a smaller blast radius.
- Access boundaries remain explicit and auditable across the platform.
