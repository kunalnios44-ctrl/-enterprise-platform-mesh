# ADR-018: Guardrailed Remediation and Explicit Approval Boundaries

## Context
Automated remediation scripts and fast CI/CD pipelines can accelerate recovery, but acting without clear validation gates or approval boundaries can apply unintended changes during uncertain states.

## Decision
1. Require passing deterministic checks and explicit threshold validation before allowing automated or high-impact changes to proceed.
2. Separate read/verification checks from mutating actions so failures halt cleanly without partial state changes.
3. Keep decision criteria documented and reviewable alongside the guardrails that enforce them.

## Consequences
- Recovery and automation stay safe and predictable under changing conditions.
- High-impact transitions remain gated behind clear, verifiable signals.
- 
