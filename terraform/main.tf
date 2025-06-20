provider "aws" {
  region                   = "us-east-1"
  shared_credentials_files = ["../_credentials/aws_learner_lab_credentials"]
  profile                  = "awslearnerlab"
}

resource "aws_instance" "api" {
  ami           = "ami-02f7c3a0c32f3f59e"
  key_name      = "vockey"
  instance_type = "t2.micro"

  tags = {
    Name = "mlops-api"
  }

  vpc_security_group_ids = [aws_security_group.allow_ssh_http.id]
}

resource "aws_instance" "training" {
  ami           = "ami-02f7c3a0c32f3f59e"
  key_name      = "vockey"
  instance_type = "t2.micro"

  tags = {
    Name = "mlops-training"
  }

  vpc_security_group_ids = [aws_security_group.allow_ssh_http.id]
}

resource "aws_security_group" "allow_ssh_http" {
  name        = "allow_ssh_http"
  description = "Allow SSH and HTTP"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5001
    to_port     = 5001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
