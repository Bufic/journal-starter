module "vpc" {
  source              = "./modules/vpc"
  vpc_cidr            = "10.0.0.0/16"
  public_subnet_cidr  = "10.0.1.0/24"
  private_subnet_cidr = "10.0.2.0/24"
  az_1                = "us-east-1a"
  az_2                = "us-east-1b"
}

module "security_group" {
  source  = "./modules/security_group"
  vpc_id  = module.vpc.vpc_id
}

module "ec2" {
  source             = "./modules/ec2"
  ami_id             = "ami-020cba7c55df1f615" # Amazon Linux 2 or Ubuntu
  key_name           = "three-tier"
  public_subnet_id   = module.vpc.public_subnet_id
  private_subnet_id  = module.vpc.private_subnet_id
  fastapi_sg_id      = module.security_group.fastapi_sg_id
  postgres_sg_id     = module.security_group.postgres_sg_id
  db_name            = var.db_name
  db_user            = var.db_user
  db_password        = var.db_password
}
