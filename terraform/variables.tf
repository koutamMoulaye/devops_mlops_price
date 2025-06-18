variable "aws_region" {
  description = "AWS region"
  default     = "eu-west-1"
}

variable "ami_id" {
  description = "AMI ID for the EC2 instances"
}

variable "instance_type" {
  description = "Type of EC2 instance"
  default     = "t2.micro"
}

variable "key_name" {
  description = "SSH key name to access instances"
}
