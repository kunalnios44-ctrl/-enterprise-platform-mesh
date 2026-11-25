# Enterprise Platform Mesh
**Internal Developer Platform (IDP) & Infrastructure Guardrail Reference Architecture**

A modular, policy-as-code platform engineering framework designed for multi-cloud resilience, zero-trust governance, and deterministic infrastructure validation across 9 core domains and 5 automated CI/CD pipelines.
## CI-Verified Benchmarks & Core Principles
* **CI/CD Speed & Footprint:** 9s–13s pipeline execution with an 8 KB – 21.2 KB artifact footprint and strict 1 MiB guardrail payload cap.
* **Security & Isolation:** Fail-closed by default, blast-radius isolation, and continuous DR verification.

## Repository Structure & Tech Stack
* **Structure:** Modular layout including `.github/workflows/`, `platform-guardrail/`, `security/`, `infra/`, `platform/`, `observability/`, `dr-backup/`, `tools/`, and `docs/` (19 ADRs).
* **Tech Stack:** Python (66.2%), Go (16.8%), Terraform/HCL (16.7%), Kubernetes, Helm, Kyverno, OpenTelemetry, and GitHub Actions.

## Quick Start & Contact
* **Run Verification:** `python3 tools/verify_guardrails.py --help` and `go test -v ./...` in `platform-guardrail/`.
* **GitHub:** [@kunalnios44-ctrl](https://github.com) | **Email:** kunalnios44@gmail.com
* 
