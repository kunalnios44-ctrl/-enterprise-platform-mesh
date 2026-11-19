locals {
  normalized_env = lower(trimspace(var.environment))

  common_labels = {
    platform    = var.platform_name
    managed_by  = "terraform"
    environment = local.normalized_env
    zero_trust  = "enforced"
  }
}
