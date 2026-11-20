# ADR-015: Strict Configuration Schemas and Drift Prevention

## Context
Unvalidated configuration changes or gradual drift between declared intent and active environment state can cause subtle failures that are hard to diagnose late in a release cycle.

## Decision
1. Validate configuration and guardrail payloads against explicit required fields, types, and value ranges before running checks.
2. Treat unexpected or malformed inputs as runtime/validation errors (`exit 2`) rather than silently guessing defaults.
3. Keep infrastructure, observability, rollout, and security rules aligned with documented baselines and automated tests.

## Consequences
- Configuration mistakes fail early with clear diagnostics.
- Environment behavior stays closer to intended baselines across changes.
- 
