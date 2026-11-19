variable "environment" {
  description = "Target platform environment name (e.g., dev, staging, prod)."
  type        = string
  default     = "prod"
}

variable "platform_name" {
  description = "Global platform engineering identifier."
  type        = string
  default     = "global-platform-engineering"
}

variable "supported_clouds" {
  description = "Multi-cloud providers aligned with platform boundaries."
  type        = list(string)
  default     = ["aws", "azure", "gcp"]
}

variable "kubernetes_distributions" {
  description = "Managed Kubernetes distributions across cloud providers."
  type        = list(string)
  default     = ["eks", "aks", "gke"]
}
