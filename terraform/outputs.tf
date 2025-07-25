output "db_endpoint" {
  description = "Postgres RDS endpoint"
  value       = aws_db_instance.hello_doc_db.address
}

output "ecs_service_name" {
  description = "ECS Service Name"
  value       = aws_ecs_service.app.name
} 