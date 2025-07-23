terraform {
  backend "s3" {
    bucket         = "journal-api-terraform-state-bucket"
    key            = "journal-api/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
  }
}
