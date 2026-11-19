output "dev_platform_labels" {
  description = "Development standardized platform labels."
  value       = module.baseline.platform_labels
}

output "dev_cluster_inventory" {
  description = "Development EKS, AKS, and GKE cluster inventory."
  value       = module.multi_cloud_k8s.cluster_inventory
}
