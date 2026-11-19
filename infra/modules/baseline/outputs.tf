output "platform_labels" {
  description = "Standardized metadata labels for multi-cloud platform resources."
  value       = local.common_labels
}

output "supported_clouds" {
  description = "Active multi-cloud provider list."
  value       = var.supported_clouds
}

output "kubernetes_distributions" {
  description = "Active managed Kubernetes targets."
  value       = var.kubernetes_distributions
}
