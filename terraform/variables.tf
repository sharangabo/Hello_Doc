variable "aws_region" {
  description = "AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "app_name" {
  description = "Name of the application and ECS resources."
  type        = string
  default     = "hello-doc"
}

variable "db_name" {
  description = "Database name for Postgres."
  type        = string
  default     = "hello_doc"
}

variable "db_user" {
  description = "Database user for Postgres."
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Database password for Postgres."
  type        = string
  default     = "postgres"
  sensitive   = true
} 