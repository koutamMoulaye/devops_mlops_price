output "api_public_ip" {
  value = aws_instance.api.public_ip
}

output "training_public_ip" {
  value = aws_instance.training.public_ip
}
