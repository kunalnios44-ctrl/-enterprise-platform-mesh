
<div align="center">

# Enterprise Platform Mesh

**Cloud Platform Engineering · DevSecOps Pipelines · Go Guardrails · Hardened Payment API**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-0F1689?style=flat-square&logo=helm&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

[Platform Guardrail CI](https://github.com/kunalnios44-ctrl/enterprise-platform-mesh)
· [CI Zero-Trust Gate](https://github.com/kunalnios44-ctrl/enterprise-platform-mesh)
· [Container Signing GitOps](https://github.com/kunalnios44-ctrl/enterprise-platform-mesh)
· [Multi-Cloud Observability](https://github.com/kunalnios44-ctrl/enterprise-platform-mesh)
· [Backup & DR Verification](https://github.com/kunalnios44-ctrl/enterprise-platform-mesh)
· [Payment Core DevSecOps](https://github.com/kunalnios44-ctrl/enterprise-platform-mesh)

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
emial ✉️ kunalnios44@gmail.com
