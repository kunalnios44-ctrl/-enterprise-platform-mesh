variable "platform_name" {
  description = "Platform identifier inherited from baseline."
  type        = string
}

variable "environment" {
  description = "Target deployment environment (e.g., dev, staging, prod)."
  type        = string
}

variable "cloud_regions" {
  description = "Primary regions across AWS, Azure, and Google Cloud."
  type        = map(string)
  default = {
    aws   = "ap-south-1"
    azure = "centralindia"
    gcp   = "asia-south1"
  }
}

variable "clusters" {
  description = "Managed Kubernetes cluster definitions for EKS, AKS, and GKE."
  type = map(object({
    cloud        = string
    distribution = string
    region       = string
  }))
  default = {
    eks-primary = {
      cloud        = "aws"
      distribution = "EKS"
      region       = "ap-south-1"
    }
    aks-primary = {
      cloud        = "azure"
      distribution = "AKS"
      region       = "centralindia"
    }
    gke-primary = {
      cloud        = "gcp"
      distribution = "GKE"
      region       = "asia-south1"
    }
  }
}
