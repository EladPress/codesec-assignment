output "alb_url" {
  description = "Public URL of the latency service behind the ALB."
  value       = "http://${aws_lb.this.dns_name}"
}

output "connect_command" {
  description = "Open a shell in a running task (needs the SSM Session Manager plugin)."
  value = join(" ", [
    "aws ecs execute-command --region ${var.region}",
    "--cluster ${aws_ecs_cluster.this.name}",
    "--container codsec --interactive --command /bin/sh",
    "--task {TASK_ID}",
  ])
}
