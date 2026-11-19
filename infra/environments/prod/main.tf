module "baseline" {
  source        = "../../modules/baseline"
  platform_name = var.platform_name
  environment   = var.environment
}

module "multi_cloud_k8s" {
  source        = "../../modules/multi-cloud-k8s"
  platform_name = var.platform_name
  environment   = var.environment
}
