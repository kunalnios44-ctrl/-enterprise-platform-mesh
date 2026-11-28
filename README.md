<div align="center">

# Enterprise Platform Mesh

**Lightweight Cloud Platform, DevSecOps Pipelines, Go Guardrails & Hardened Payment API**

![Python](https://shields.io)
![FastAPI](https://shields.io)
![Go](https://shields.io)
![Terraform](https://shields.io)
![Kubernetes](https://shields.io)
![Helm](https://shields.io)
![Docker](https://shields.io)
![GitHub Actions](https://shields.io)

[![Platform Guardrail CI/CD](https://github.com)](https://github.com)
[![CI Zero-Trust Gate](https://github.com)](https://github.com)
[![Container Signing GitOps](https://github.com)](https://github.com)
[![Multi-Cloud Observability](https://github.com)](https://github.com)
[![Backup & DR Verification](https://github.com)](https://github.com)
[![Payment Core DevSecOps](https://github.com)](https://github.com)

</div>

---

## Honest Proof of Work

This repository is built with a minimal footprint (`10 KB – 25 KB per module`) and verified across **116 commits** and **48+ green GitHub Actions runs**:

* **Fast Green Pipelines (`~15s – 24s`):** Every CI/CD check (unit tests, Bandit SAST, `pip-audit`, and policy verification) completes in under 25 seconds.
* **Lightweight Footprint:** Follows strict dependency hygiene (`ADR-013`), keeping configs, policies, and code concise and easy to audit.
* **Iterative Work (`116 Commits`):** Built across 10 directories, 19 Architecture Decision Records (`docs/`), and 6 automated workflows.

---

## System Flow

```text
  [ GitHub Push / PR ] ──► [ Fast CI/CD Security Gates (~15s-24s) ]
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
  [ K8s + Helm ]             [ Go Guardrails ]           [ Kyverno Rules ]
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     ▼
                      [ Payment Core API (FastAPI) ]
```

---

## Repository Modules (`10 Folders`)

| Folder | Tools Used | What Was Built |
| :--- | :--- | :--- |
| **`apps/payment-core/`** | Python, FastAPI, SQLite, Docker | Payment API prototype with mandatory `PAYMENT_API_KEY` check, `Decimal` math (`0.00 < amount <= 10000.00`), ISO-13616 Mod-97 IBAN validation, EU region allowlist, SQLite idempotency, non-root container, and 9 Pytest tests. |
| **`platform-guardrail/`** | Go | Policy enforcement and rollout validation engine. |
| **`security/`** | Kyverno, YAML | Zero-trust workload admission rules. |
| **`.github/workflows/`** | GitHub Actions | 6 automated pipelines (`48+` green runs) for tests, security scans, signing, observability, and DR verification. |
| **`infra/` & `platform/`** | Terraform, Kubernetes, Helm | Multi-region EU Terraform configurations and K8s/Helm deployment manifests. |
| **`observability/` & `dr-backup/`** | Telemetry, Scripts | Metrics/logging checks and automated backup-restore verification scripts. |
| **`docs/` & `tools/`** | Markdown, CLI | 19 Architecture Decision Records (`ADR-001` to `ADR-019`) and operational runbooks. |

---

## Verify Locally

```bash
cd apps/payment-core
PAYMENT_API_KEY="local-test-key" pytest -v
bandit -r main.py -ll
pip-audit -r requirements.txt
```

> *Note: A personal hands-on engineering prototype built to practice platform automation and API hardening—not a live banking or payment system.*

---

<div align="center">

**Kunal Kashyap**  
[github.com/kunalnios44-ctrl/enterprise-platform-mesh](https://github.com/kunalnios44-ctrl/enterprise-platform-mesh)

</div>
