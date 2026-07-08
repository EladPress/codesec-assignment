terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region

  # Applied to every resource that supports tags, so individual resources
  # only need to set their own Name.
  default_tags {
    tags = {
      Project     = "codsec-assignment"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
