resource "aws_instance" "fastapi" {
  ami           = var.ami_id
  instance_type = "t2.micro"
  subnet_id     = var.public_subnet_id
  security_groups = [var.fastapi_sg_id]
  key_name      = var.key_name

  tags = {
    Name = "FastAPI Server"
  }

}

resource "aws_instance" "postgres" {
  ami           = var.ami_id
  instance_type = "t2.micro"
  subnet_id     = var.public_subnet_id
  security_groups = [var.postgres_sg_id]
  key_name      = var.key_name
  user_data = templatefile("${path.module}/postgres.sh", {
  db_name     = var.db_name,
  db_user     = var.db_user,
  db_password = var.db_password
})


  tags = {
    Name = "Postgres Server"
  }
}
