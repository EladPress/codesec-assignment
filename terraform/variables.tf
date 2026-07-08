variable "region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "il-central-1"
}

variable "container_image" {
  description = "Container image (repo:tag) the ECS task runs. Point this at a tag the CI pipeline pushed."
  type        = string
  default     = "eladpress/codsec-assignment:main-14"
}

variable "container_port" {
  description = "Port the container (uvicorn) listens on."
  type        = number
  default     = 8000
}

variable "environment" {
  description = "Environment tag applied to all resources."
  type        = string
  default     = "Lab"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "desired_count" {
  description = "Baseline number of running tasks. Kept at 1 to minimise cost."
  type        = number
  default     = 1
}
