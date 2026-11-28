terraform {
  required_version = ">= 1.6.0"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}

variable "guardrail_namespace" {
  type        = string
  description = "Target Kubernetes namespace for the chaos-resilience control plane"
  default     = "platform-guardrail"
}

variable "create_namespace" {
  type        = bool
  description = "Whether Terraform should create the target namespace"
  default     = false
}

resource "kubernetes_namespace_v1" "guardrail" {
  count = var.create_namespace ? 1 : 0

  metadata {
    name = var.guardrail_namespace
    labels = {
      "pod-security.kubernetes.io/enforce" = "privileged"
    }
  }
}

resource "kubernetes_resource_quota_v1" "guardrail_quota" {
  metadata {
    name      = "guardrail-compute-quota"
    namespace = var.guardrail_namespace
  }

  spec {
    hard = {
      "requests.cpu"    = "4"
      "requests.memory" = "4Gi"
      "limits.cpu"      = "8"
      "limits.memory"   = "8Gi"
      pods              = "50"
    }
  }

  depends_on = [kubernetes_namespace_v1.guardrail]
}

resource "kubernetes_limit_range_v1" "guardrail_defaults" {
  metadata {
    name      = "guardrail-limit-range"
    namespace = var.guardrail_namespace
  }

  spec {
    limit {
      type = "Container"

      default = {
        cpu    = "500m"
        memory = "256Mi"
      }

      default_request = {
        cpu    = "100m"
        memory = "64Mi"
      }
    }
  }

  depends_on = [kubernetes_namespace_v1.guardrail]
}

resource "kubernetes_network_policy_v1" "namespace_baseline" {
  metadata {
    name      = "guardrail-pod-baseline"
    namespace = var.guardrail_namespace
  }

  spec {
    pod_selector {}

    policy_types = ["Ingress", "Egress"]

    ingress {
      ports {
        protocol = "TCP"
        port     = 8443
      }
    }

    egress {
      to {
        namespace_selector {
          match_labels = {
            "kubernetes.io/metadata.name" = "kube-system"
          }
        }
      }
      ports {
        protocol = "UDP"
        port     = 53
      }
      ports {
        protocol = "TCP"
        port     = 53
      }
    }

    egress {
      ports {
        protocol = "TCP"
        port     = 443
      }
    }
  }

  depends_on = [kubernetes_namespace_v1.guardrail]
}
