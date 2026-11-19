locals {
  normalized_env = lower(trimspace(var.environment))

  cluster_inventory = {
    for k, c in var.clusters : k => {
      cloud        = lower(c.cloud)
      distribution = upper(c.distribution)
      region       = c.region
      environment  = local.normalized_env
      platform     = var.platform_name
    }
  }
}
