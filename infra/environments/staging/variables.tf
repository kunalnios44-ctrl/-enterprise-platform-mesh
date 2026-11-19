variable "platform_name" {
  description = "Platform identifier for the staging environment."
  type        = string
  default     = "global-platform-engineering"
}

variable "environment" {
  description = "Environment name for staging."
  type        = string
  default     = "staging"
}
