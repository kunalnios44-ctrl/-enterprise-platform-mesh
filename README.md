<div align="center">

# Enterprise Platform Mesh

**Cloud Platform Engineering • DevSecOps Pipelines • Go Guardrails • Hardened Payment API**

<!-- Tech Stack Badges -->
<p>
  <img src="https://shields.io" alt="Python" />
  <img src="https://shields.io" alt="FastAPI" />
  <img src="https://shields.io" alt="Go" />
  <img src="https://shields.io" alt="Terraform" />
  <img src="https://shields.io" alt="Kubernetes" />
  <img src="https://shields.io" alt="Helm" />
  <img src="https://shields.io" alt="Docker" />
</p>

<!-- Live GitHub Actions Workflow Badges -->
<p>
  <a href="https://github.com">
    <img src="https://github.com/badge.svg" alt="Platform Guardrail CI" />
  </a>
  <a href="https://github.com">
    <img src="https://github.com/badge.svg" alt="CI Zero-Trust Gate" />
  </a>
  <a href="https://github.com">
    <img src="https://github.com/badge.svg" alt="Container Signing GitOps" />
  </a>
  <br />
  <a href="https://github.com">
    <img src="https://github.com/badge.svg" alt="Multi-Cloud Observability" />
  </a>
  <a href="https://github.com">
    <img src="https://github.com/badge.svg" alt="Backup & DR Verification" />
  </a>
  <a href="https://github.com">
    <img src="https://github.com/badge.svg" alt="Payment Core DevSecOps" />
  </a>
</p>

</div>

---

## Overview

A practical platform engineering repository built around automated delivery, policy guardrails, workload security, observability, disaster recovery, and a security-hardened payment API prototype. Every pipeline executes automated tests, SAST/SCA scans, policy checks, and container validations.

---

## Architecture

```text
                    ┌─────────────────────────┐
                    │       GitHub PR/Push    │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   CI/CD Security Gates  │
                    │  Tests • SAST • SCA     │
                    │  Policy • Containers    │
                    └────────────┬────────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               ▼                 ▼                 ▼
        ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
        │   Platform  │  │   Security   │  │  Guardrails  │
        │ K8s + Helm  │  │ Zero Trust   │  │ Policy Engine│
        └──────┬──────┘  └──────┬───────┘  └──────┬───────┘
               │                 │                 │
               └─────────────────┼─────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │      Payment Core       │
                    │      (FastAPI App)      │
                    └────────────┬────────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               ▼                 ▼                 ▼
        ┌─────────────┐  ┌──────────────┐  ┌──────────────┐
        │Observability│  │ Backup / DR  │  │ Multi-Cloud  │
        │ Metrics/Logs│  │ Verification │  │ Terraform    │
        └─────────────┘  └──────────────┘  └──────────────┘
```

---

## Repository Structure

```text
enterprise-platform-mesh/
├── .github/workflows/       # 6 CI/CD & verification pipelines
├── apps/payment-core/       # FastAPI payment prototype, tests & Dockerfile
├── docs/                    # Architecture Decision Records (ADR-001 to ADR-019)
├── dr-backup/               # Backup & disaster recovery verification scripts
├── infra/                   # Multi-cloud Terraform configurations
├── observability/           # Metrics, telemetry, and logging configs
├── platform/                # Kubernetes & Helm deployment charts
├── platform-guardrail/      # Go-based policy enforcement engine
├── security/                # Zero-trust policies & Kyverno admission rules
└── tools/                   # Automated verification utilities
```

---

## Payment Core Controls (`apps/payment-core`)

| Control | Implementation |
| :--- | :--- |
| **Secrets** | Mandatory `PAYMENT_API_KEY` (fail-fast startup check) |
| **Monetary Math** | Python `Decimal` (`0.00 < amount <= 10000.00`) |
| **IBAN Validation** | ISO-13616 Mod-97 checksum verification |
| **Region Enforcement** | EU server-side allowlist |
| **Idempotency** | Persistent SQLite unique constraints & collision handling |
| **Container** | Slim Python image running as non-root user + `/health` check |
| **Security & Tests** | Pytest, Bandit (SAST), and `pip-audit` (SCA) |

---

## CI/CD Pipelines (`.github/workflows`)

| Workflow File | Purpose |
| :--- | :--- |
| `platform-guardrail-ci.yml` | Runs Go guardrail tests and policy checks |
| `ci-zero-trust-gate.yml` | Enforces zero-trust security rules |
| `container-signing-gitops.yml` | Container signing and GitOps manifest validation |
| `multi-cloud-observability.yml` | Validates metrics and logging configurations |
| `backup-dr-verification.yml` | Executes backup integrity and recovery tests |
| `payment-core-devsecops.yml` | Runs Pytest, Bandit, `pip-audit`, and Docker smoke tests |

---

## Local Verification

```bash
# 1. Navigate to payment-core
cd apps/payment-core

# 2. Run unit & concurrency tests
PAYMENT_API_KEY="local-test-key" pytest -v

# 3. Run security & dependency scans
bandit -r main.py -ll
pip-audit -r requirements.txt

# 4. Start the API locally (Swagger UI available at /docs)
PAYMENT_API_KEY="local-test-key" SERVER_REGION="eu-north-1" uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Scope & Maintainer

> **Note:** This repository is an engineering prototype built to practice platform automation, security controls, and recovery verification. It is not a live banking or regulated payment system.

**Kunal Kashyap** — [@kunalnios44-ctrl](https://github.com/kunalnios44-ctrl)
