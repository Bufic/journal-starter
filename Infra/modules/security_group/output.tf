output "fastapi_sg_id" {
  value = aws_security_group.fastapi_sg.id
}

output "postgres_sg_id" {
  value = aws_security_group.postgres_sg.id
}
