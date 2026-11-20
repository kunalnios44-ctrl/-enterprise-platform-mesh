# Enterprise Platform Mesh 🚀

An end-to-end **Platform Engineering & DevSecOps architecture** demonstrating multi-cloud infrastructure provisioning, zero-trust security guardrails, signed container GitOps delivery, full-stack observability, and automated disaster recovery verification across **19 industry-standard tools and 5 automated CI/CD pipelines**.

🔗 **Repository:** [://github.com](https://://github.com)

---

## ✈️ Open to On-Site Relocation (Nordic Region)

I am actively seeking **On-Site  Platform Engineer / DevSecOps / Cloud Infrastructure** roles with **Relocation & Work Visa Sponsorship** in the Nordic region.
* **Target Countries (On-Site Only):** 🇩🇰 **Denmark** | 🇸🇪 **Sweden** | 🇫🇮 **Finland**
* **Direct Contact:** 📧 `kunalnios44@gmail.com`

---

## 🏗️ High-Level Architecture Flow

```text
[ Developer / Backstage IDP ]
          │
          ▼
[ GitHub Actions (5 Automated Pipelines) ]
   ├──► Static & Policy Checks (Semgrep + Platform Guardrails)
   ├──► Keyless Cloud Auth (OIDC + Least-Privilege IAM/RBAC)
   ├──► Container Build, Scan & Sign (Docker + Trivy + Cosign)
   └──► GitOps Delivery ──► Multi-Cloud Kubernetes (AWS EKS | Azure AKS | GCP GKE)
                                   │
          ┌────────────────────────┼────────────────────────┐
          ▼                        ▼                        ▼
[ Terraform (HCL) IaC ]   [ Observability Stack ]   [ Python DR Automation ]
   (Multi-Cloud Infra)     (Prometheus, Grafana,     (Automated Backups &
                             OpenTelemetry)            Recovery Verification)
```

---

## 🛠️ Tech Stack (19 Integrated Tools)

* **Multi-Cloud & Infrastructure:** AWS, Azure, Google Cloud (GCP), Terraform (HCL), Docker, Kubernetes (EKS, AKS, GKE), Helm
* **CI/CD & Developer Experience:** GitHub Actions, GitOps, Backstage (Internal Developer Portal)
* **Zero-Trust Security & Supply Chain:** IAM / RBAC, OIDC (Keyless Authentication), Semgrep (SAST), Trivy (Container & FS Scanning), Cosign (Image Signing)
* **Observability & Disaster Recovery:** Prometheus, Grafana, OpenTelemetry, Python (Custom DR & Backup Verification)

---

## ⚙️ Automated CI/CD Pipelines (5 Verified Workflows)

1. **Platform Guardrail CI/CD (`platform-guardrail-ci.yml`):** Enforces platform policies, runs verification checks, and packages validated deployment artifacts.
2. **Container Signing & GitOps Delivery:** Scans container images for vulnerabilities using **Trivy**, cryptographically signs them with **Cosign**, and triggers **GitOps** rollout.
3. **Multi-Cloud Infra & Observability Sync:** Synchronizes infrastructure states and monitoring configurations across **AWS, Azure, and GCP**.
4. **Backup & Disaster Recovery Verification:** Executes custom **Python** automation to verify snapshots, backups, and disaster recovery readiness.
5. **Security & IAM Compliance Checks:** Validates least-privilege **IAM/RBAC** policies and performs static code analysis using **Semgrep**.

---

## 📂 Repository Structure

* `.github/workflows/` – Automated CI/CD, security, and DR verification pipelines
* `infra/` – Multi-cloud Terraform (HCL) infrastructure configurations
* `platform/` – Kubernetes manifests, Helm charts, and Backstage definitions
* `platform-guardrail/` – Policy-as-code and platform guardrail enforcement rules
* `security/` – IAM/RBAC policies, OIDC federation, and scanning setups
* `observability/` – Prometheus, Grafana, and OpenTelemetry monitoring configurations
* `dr-backup/` – Python scripts for automated backup and disaster recovery testing
* `docs/` – Architecture documentation and operational runbooks

---

## 📬 Let's Connect

If you are hiring for **On-Site Platform Engineering, Cloud Infrastructure, or DevSecOps** roles in **Denmark, Sweden, or Finland**, feel free to reach out directly:

* **Email:** [kunalnios44@gmail.com](mailto:kunalnios44@gmail.com)
* **GitHub:** [@kunalnios44-ctrl](https://github.com)
