output "cloud_regions" {
  description = "Configured regions across AWS, Azure, and Google Cloud."
  value       = var.cloud_regions
}

output "cluster_inventory" {
  description = "Normalized managed Kubernetes cluster inventory (EKS, AKS, GKE)."
  value       = local.cluster_inventory
}
