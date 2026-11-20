# ADR-014: Incident Triage and Blameless Postmortem Discipline

## Context
When incidents or guardrail blocks occur in production or CI/CD workflows, ad-hoc responses and missing follow-ups can allow the same failure mode to repeat.

## Decision
1. Triage incidents using clear severity signals, guardrail exit codes (`0`, `1`, `2`), and verified operational telemetry before taking corrective action.
2. Focus postmortems on system gaps, unclear boundaries, or missing checks rather than blaming individuals.
3. Convert key postmortem findings into concrete guardrails, tests, or documentation updates.

## Consequences
- Teams resolve issues faster with clearer root-cause visibility.
- Repeated failure modes are systematically reduced over time.
