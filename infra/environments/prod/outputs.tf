output "prod_platform_labels" {
  description = "Production standardized platform labels."
  value       = module.baseline.platform_labels
}

output "prod_cluster_inventory" {
  description = "Production EKS, AKS, and GKE cluster inventory."
  value       = module.multi_cloud_k8s.cluster_inventory
}
