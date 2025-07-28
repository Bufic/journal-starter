variable "aws_region" {
  type        = string
  description = "AWS region"
}

variable "db_name" {
  description = "Name of the PostgreSQL database"
  type        = string
}

variable "db_user" {
  description = "PostgreSQL username"
  type        = string
}

variable "db_password" {
  description = "Password for the PostgreSQL user"
  type        = string
  sensitive   = true
}