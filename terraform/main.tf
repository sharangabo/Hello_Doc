resource "aws_db_instance" "hello_doc_db" {
  allocated_storage    = 20
  engine              = "postgres"
  engine_version      = "13.4"
  instance_class      = "db.t3.micro"
  db_name             = var.db_name
  username            = var.db_user
  password            = var.db_password
  parameter_group_name = "default.postgres13"
  skip_final_snapshot = true
}

resource "aws_ecs_cluster" "main" {
  name = var.app_name
}

resource "aws_ecs_task_definition" "app" {
  family                   = var.app_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  container_definitions    = "[]"
}

resource "aws_ecs_service" "app" {
  name            = var.app_name
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = ["subnet-12345678"]
    assign_public_ip = true
  }
  depends_on = [aws_ecs_cluster.main]
} 