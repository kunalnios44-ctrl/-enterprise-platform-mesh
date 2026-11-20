# ADR-011: Progressive Delivery and Canary Rollout Safety

## Context
Rolling out application changes all at once across production instances increases blast radius when a release introduces latency spikes, errors, or configuration issues.

## Decision
1. Prefer controlled progressive rollouts with explicit traffic caps and minimum replica counts where applicable.
2. Require passing pre-rollout checks and healthy observability signals before expanding rollout scope.
3. Keep rollout validation rules deterministic so unsafe configurations fail before execution.

## Consequences
- Potential regressions are detected early on a limited slice of traffic.
- Production availability remains better protected during active releases.
