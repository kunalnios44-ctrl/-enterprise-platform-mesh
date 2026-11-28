
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

</div>)
Enterprise Platform Mesh

A cloud-native platform engineering project focused on Kubernetes security, infrastructure automation, workload resilience, and operational verification.

This repository brings together platform guardrails, application security, CI/CD automation, observability, disaster recovery, and eBPF-based network resilience.

Project Overview

The project contains the following engineering areas:

- Kubernetes runtime guardrails
- Zero Trust policy enforcement
- Admission webhook
- Go-based platform agent and controller
- eBPF network resilience
- Terraform infrastructure configuration
- CI/CD and supply-chain verification
- Container signing and GitOps
- Multi-cloud observability
- Backup and disaster recovery
- Payment Core application

Architecture

flowchart TD
    A[Developer Changes] --> B[GitHub Actions]
    B --> C[CI Verification]
    C --> D[Security and Policy Gates]
    D --> E[Platform Guardrails]
    E --> F[Kubernetes Workloads]
    F --> G[Platform Agent]
    G --> H[eBPF Network Controls]
    F --> I[Observability]
    I --> J[Operational Verification]
    J --> K[Resilience and Recovery]
    L[Terraform] --> E
    M[Payment Core] --> F

Repository Structure

enterprise-platform-mesh/
├── .github/
│   └── workflows/
├── apps/
│   └── payment-core/
├── bpf/
│   └── chaos_tc.c
├── cmd/
│   └── agent/
├── deploy/
├── dr-backup/
├── infra/
├── internal/
├── observability/
├── platform/
├── platform-guardrail/
├── security/
├── tools/
└── README.md

Platform Guardrails

The platform guardrail implementation covers:

- Policy validation
- Terraform plan verification
- SLO evaluation
- Rollout validation
- Kubernetes runtime policies
- OIDC and RBAC controls
- Zero Trust configuration
- Configuration drift controls

Chaos Resilience and eBPF

The repository includes a Linux eBPF Traffic Control program.

"bpf/chaos_tc.c" implements network packet inspection and policy-based packet manipulation.

Implemented areas include:

- TC egress processing
- IPv4 and TCP inspection
- Destination-port policy lookup
- Configurable packet-drop behaviour
- TCP control-flag protection
- Policy statistics

The agent and controller provide supporting components for managing resilience policies.

Kubernetes

Kubernetes-related engineering includes:

- Runtime guardrail manifests
- Admission webhook
- Service account configuration
- Namespace security boundaries
- Policy enforcement
- Chaos resilience agent deployment

Security and Supply Chain

Security-related components cover:

- Zero Trust gates
- Container signing
- Supply-chain attestations
- Secretless authentication design
- Least-privilege access
- Dependency verification
- Artifact integrity
- Admission policies

Infrastructure

Terraform and automation support infrastructure configuration and verification.

The repository also includes work around multi-cloud infrastructure controls and deployment configuration.

Payment Core

"apps/payment-core" is the application workload used to exercise platform security and delivery controls.

Its documented areas include:

- Payment processing
- Idempotency
- Monetary value handling
- IBAN validation
- EU region restrictions
- Application testing
- Container security

Observability and Disaster Recovery

Observability configuration includes:

- Prometheus
- Grafana
- OpenTelemetry Collector
- Telemetry sampling guardrails
- SLO verification

Disaster recovery work covers backup verification, recovery objectives, and operational readiness checks.

CI/CD

GitHub Actions workflows cover:

- Platform verification
- Zero Trust checks
- Container signing and GitOps
- Multi-cloud observability
- Backup and disaster recovery
- Payment Core security
- Repository verification

Workflow results are available under the repository's Actions tab.

"View GitHub Actions" (https://github.com/kunalnios44-ctrl/enterprise-platform-mesh/actions)

Architecture Decision Records

The repository contains ADR-001 through ADR-019 documenting decisions around:

- Guardrail validation
- Zero Trust supply chain
- Disaster recovery and SLOs
- CI verification
- Multi-cloud infrastructure
- Failure isolation
- Release promotion
- Telemetry and auditability
- Secretless authentication
- Immutable artifacts
- Progressive delivery
- Capacity management
- Dependency hygiene
- Incident response
- Configuration management
- Least-privilege IAM and RBAC

Technology Stack

Technology| Purpose
Python| Automation, policy checks and testing
Go| Agent and platform components
HCL| Terraform configuration
C| eBPF network processing
Docker| Containerization
Kubernetes| Workload orchestration
GitHub Actions| CI/CD
Prometheus| Metrics
Grafana| Monitoring
OpenTelemetry| Telemetry

GitHub Language Distribution

Language| Share
Python| 57%
Go| 25.8%
HCL| 11.7%
C| 4.4%
Dockerfile| 1.1%

Distribution reported by GitHub. Percentages represent repository language composition, not test coverage.

Validation

The repository includes automated workflows and component-specific tests.

Basic Git checks:

git status
git diff --check

Additional validation depends on the component being changed and its required tooling.

Development Status

This is an actively developed engineering project.

Successful CI runs demonstrate that configured checks passed. Production deployment, multi-region operation, disaster recovery performance, and runtime security effectiveness require separate environment-level validation.

Author

Kunal Kashyap

Cloud Infrastructure | Platform Engineering | DevSecOps

"GitHub Profile" (https://github.com/kunalnios44-ctrl)

"Project Repository" (https://github.com/kunalnios44-ctrl/enterprise-platform-mesh)
emial.✉️kunalnios44@gmail.com


