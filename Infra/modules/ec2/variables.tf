variable "ami_id" {}
variable "key_name" {}
variable "public_subnet_id" {}
variable "private_subnet_id" {}
variable "fastapi_sg_id" {}
variable "postgres_sg_id" {}

variable "db_name" {
  type        = string
  description = "Name of the PostgreSQL database"
}

variable "db_user" {
  type        = string
  description = "PostgreSQL username"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "Password for the PostgreSQL user"
}
