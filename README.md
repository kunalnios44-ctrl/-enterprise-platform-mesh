# Enterprise Platform Mesh

**Internal Developer Platform (IDP), Security-Hardened Payment Core & Infrastructure Guardrail Architecture**

[![Platform Guardrail CI/CD](https://github.com)](https://github.com)
[![CI Zero-Trust Gate](https://github.com)](https://github.com)
[![Container Signing GitOps](https://github.com)](https://github.com)
[![Multi-Cloud Observability](https://github.com)](https://github.com)
[![Backup & DR Verification](https://github.com)](https://github.com)
[![Payment Core DevSecOps](https://github.com)](https://github.com)

A modular, policy-as-code platform engineering and DevSecOps repository combining multi-cloud infrastructure guardrails, zero-trust CI/CD gates, and a security-hardened FinTech payment API prototype across **10 core domains**, **6 automated GitHub Actions pipelines**, and **115+ iterative commits**.

---

## Verifiable Engineering Evidence (6 Automated Pipelines)

Every badge above links directly to live execution logs in the [GitHub Actions](https://github.com) tab:

| # | Workflow File | Verification Scope |
| :--- | :--- | :--- |
| **1** | `platform-guardrail-ci.yml` | Validates Go guardrail engine unit tests and Python policy verification scripts. |
| **2** | `ci-zero-trust-gate.yml` | Enforces security policy gates before allowing workload promotion. |
| **3** | `container-signing-gitops.yml` | Verifies supply-chain container signing and GitOps delivery manifests. |
| **4** | `multi-cloud-observability.yml` | Validates telemetry, metrics, and observability configuration schemas. |
| **5** | `backup-dr-verification.yml` | Tests disaster recovery and backup integrity procedures. |
| **6** | `payment-core-devsecops.yml` | Runs 9 Pytest security/concurrency tests, Bandit (SAST), `pip-audit` (SCA), non-root Docker build, and live `/health` container smoke tests. |

---

## Repository Architecture (10 Core Domains)

```text
-enterprise-platform-mesh/
├── .github/workflows/       # 6 Automated CI/CD, Zero-Trust & DevSecOps Verification Pipelines
├── apps/payment-core/       # Hardened Payment Core API Prototype (FastAPI, SQLite, Docker)
├── docs/                    # 19 Architecture Decision Records (ADRs) & Technical Specs
├── dr-backup/               # Disaster Recovery & Backup Verification Scripts
├── infra/                   # Multi-Cloud Infrastructure-as-Code (Terraform)
├── observability/           # Telemetry, Metrics & Logging Configurations
├── platform/                # Kubernetes & Helm Deployment Manifests
├── platform-guardrail/      # Go-based Policy & Guardrail Enforcement Engine
├── security/                # Zero-Trust Security Policies & Kyverno Rules
└── tools/                   # Automated Guardrail Verification Utilities
```

---

## Featured Workload: `apps/payment-core` (v3.2.1)

A security-focused payment processing API prototype engineered to demonstrate defensive backend and DevSecOps controls:

| Control Area | Technical Implementation |
| :--- | :--- |
| **Fail-Fast Secrets** | Enforces mandatory `PAYMENT_API_KEY` at startup; zero hardcoded fallback secrets. |
| **Monetary Precision** | Uses `Decimal` arithmetic (`0.00 < amount <= 10000.00`) to eliminate floating-point rounding bugs. |
| **IBAN Checksum Integrity** | Normalizes IBAN strings and validates structure plus **ISO-13616 Mod-97 checksums**. |
| **EU Region Allowlist** | Server-side enforcement (`eu-north-1`, `eu-west-1`, `eu-central-1`, `eu-south-1`) blocking client region spoofing. |
| **Concurrency-Safe Idempotency** | Persistent SQLite storage with `PRIMARY KEY` constraints and `IntegrityError` duplicate collision handling. |
| **Hardened Container** | Slim Python 3.11 Docker image running as non-root `appuser` with active HTTP `/health` probes. |

> **Honest Scope Note:** `apps/payment-core` is a DevSecOps engineering prototype built to demonstrate defensive API controls and automated verification workflows—not a licensed banking or live payment settlement processor.

---

## Live Interactive Demo (Run in Browser or Locally)

Reviewers can launch an interactive Swagger UI (`/docs`) and test live API requests in under 60 seconds:

### Option A: One-Click Cloud Demo (GitHub Codespaces)
1. Click **Code** $\rightarrow$ **Codespaces** $\rightarrow$ **Create codespace on main** at the top of this repository.
2. Once the terminal loads, start the live server:
   ```bash
   cd apps/payment-core && pip install -r requirements.txt
   PAYMENT_API_KEY="demo-eu-key-2026" SERVER_REGION="eu-north-1" uvicorn main:app --host 0.0.0.0 --port 8000
   ```
3. Open the forwarded port **8000** and append **`/docs`** to test live payments, IBAN Mod-97 rejection, and idempotency replay directly in your browser.

### Option B: Run Automated Verification Suite Locally
```bash
# 1. Run all 9 security, IBAN checksum & concurrency tests
cd apps/payment-core
PAYMENT_API_KEY="local-test-key" pytest -v

# 2. Run static security analysis (SAST) & dependency audit (SCA)
bandit -r main.py -ll
pip-audit -r requirements.txt
```

---

## Contact & Maintainer

* **GitHub:** [@kunalnios44-ctrl](https://github.com)
* **Email:** kunalnios44@gmail.com
* 
