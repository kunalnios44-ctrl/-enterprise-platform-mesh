output "staging_platform_labels" {
  description = "Staging standardized platform labels."
  value       = module.baseline.platform_labels
}

output "staging_cluster_inventory" {
  description = "Staging EKS, AKS, and GKE cluster inventory."
  value       = module.multi_cloud_k8s.cluster_inventory
}
