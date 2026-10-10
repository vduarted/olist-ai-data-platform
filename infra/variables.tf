variable "region" {
  type        = string
  description = "Defines the AWS region that will be used"
  default     = "us-east-2"
}

variable "project" {
  type        = string
  description = "The project name"
  default     = "olist"
}

variable "env" {
  type        = string
  description = "Deployment environment (dev or prod)"
  default     = "dev"

  validation {
    condition     = contains(["dev", "prod"], var.env)
    error_message = "Environment must be dev or prod."
  }
}

variable "aws_profile" {
  type       = string
  description = "Sets the AWS profile used on authentication."
  default    = "olist-tf"
}