variable "platform_name" {
  description = "Platform identifier for the production environment."
  type        = string
  default     = "global-platform-engineering"
}

variable "environment" {
  description = "Environment name for production."
  type        = string
  default     = "prod"
}
