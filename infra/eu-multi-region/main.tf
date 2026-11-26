terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "environment" {
  description = "Deployment environment (e.g., prod, staging)"
  type        = string
  default     = "prod"
}

variable "approved_eu_regions" {
  description = "Strict allowlist of GDPR-compliant European regions"
  type        = set(string)
  default     = ["eu-north-1", "eu-central-1", "eu-west-1"]

  validation {
    condition     = alltrue([for r in var.approved_eu_regions : startswith(r, "eu-")])
    error_message = "GDPR COMPLIANCE VIOLATION: Only European (eu-*) regions are permitted for payment-core infrastructure."
  }
}

# Primary Region: Stockholm, Sweden (Nordic Green Cloud Hub)
provider "aws" {
  alias  = "stockholm"
  region = "eu-north-1"
}

# Secondary Disaster Recovery Region: Frankfurt, Germany (EU Core)
provider "aws" {
  alias  = "frankfurt"
  region = "eu-central-1"
}

resource "aws_kms_key" "eu_payment_encryption_primary" {
  provider                = aws.stockholm
  description             = "Customer-managed KMS key for Payment Core encryption in Stockholm (eu-north-1)"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Project     = "enterprise-platform-mesh"
    Service     = "payment-core"
    Compliance  = "GDPR-Strict"
    Environment = var.environment
  }
}

resource "aws_kms_key" "eu_payment_encryption_dr" {
  provider                = aws.frankfurt
  description             = "Disaster Recovery KMS key for Payment Core in Frankfurt (eu-central-1)"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  tags = {
    Project     = "enterprise-platform-mesh"
    Service     = "payment-core"
    Compliance  = "GDPR-Strict"
    Environment = var.environment
  }
}

output "gdpr_enforced_regions" {
  description = "Verified European regions configured for active-active resilience"
  value       = var.approved_eu_regions
}
