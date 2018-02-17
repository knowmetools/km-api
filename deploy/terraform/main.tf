terraform {
  backend "s3" {
    bucket         = "km-tf-state"
    dynamodb_table = "terraformLock"
    key            = "km-api/terraform.tfstate"
    region         = "us-east-1"
  }
}


locals {
  env        = "${terraform.workspace == "default" ? "dev" : terraform.workspace}"
  app_name   = "${local.env == "production" ? "km-api" : "km-api-${local.env}"}"
  sub_domain = "${local.env == "production" ? "toolbox" : "${local.env}.toolbox"}"
}


provider "aws" {
  region = "${var.aws_region}"
}


data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

data "aws_iam_policy" "cloudwatch" {
  arn = "arn:aws:iam::656952694364:policy/CloudWatchSendLogs"
}

data "aws_iam_policy" "ses" {
  arn = "arn:aws:iam::656952694364:policy/SESSendEmails"
}

data "aws_iam_policy_document" "instance-assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

data "aws_route53_zone" "main" {
  name = "${var.route53_zone_name}"
}


// Database

resource "aws_db_instance" "main" {
  allocated_storage      = "${var.db_capacity}"
  engine                 = "postgres"
  instance_class         = "${var.db_instance_type}"
  password               = "${var.db_master_password}"
  publicly_accessible    = true
  username               = "${var.db_master_username}"
  vpc_security_group_ids = ["${aws_security_group.db.id}"]

  tags {
    Application = "${local.app_name}"
    Name        = "${local.app_name} Database"
  }
}


// EC2 Resources

resource "aws_key_pair" "deploy" {
  key_name_prefix = "${local.app_name}-deploy"
  public_key      = "${file(var.public_key_path)}"
}

resource "aws_instance" "webserver" {
  ami                    = "${data.aws_ami.ubuntu.id}"
  iam_instance_profile   = "${aws_iam_instance_profile.web.name}"
  instance_type          = "${var.web_instance_type}"
  key_name               = "${aws_key_pair.deploy.key_name}"
  vpc_security_group_ids = ["${aws_security_group.web.id}"]

  tags {
    Application = "${local.app_name}"
    Name        = "${local.app_name} Webserver"
  }
}

resource "aws_iam_instance_profile" "web" {
  name_prefix = "${local.app_name}-web"
  role        = "${aws_iam_role.web.name}"
}

resource "aws_iam_role" "web" {
  assume_role_policy = "${data.aws_iam_policy_document.instance-assume-role-policy.json}"
  name_prefix        = "${local.app_name}-web"
}

resource "aws_iam_role_policy_attachment" "cloudwatch" {
  policy_arn = "${data.aws_iam_policy.cloudwatch.arn}"
  role       = "${aws_iam_role.web.name}"
}

resource "aws_iam_role_policy_attachment" "ses" {
  policy_arn = "${data.aws_iam_policy.ses.arn}"
  role       = "${aws_iam_role.web.name}"
}

resource "aws_iam_role_policy_attachment" "static_files" {
  policy_arn = "${aws_iam_policy.static_access.arn}"
  role       = "${aws_iam_role.web.name}"
}

// Static File Storage

resource "aws_s3_bucket" "static" {
  acl           = "public-read"
  bucket_prefix = "${local.app_name}-static"
  region        = "${var.aws_region}"

  cors_rule {
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
  }

  tags {
    Application = "${local.app_name}"
    Name        = "${local.app_name} Static Files"
  }
}

resource "aws_iam_policy" "static_access" {
  description = "Allows access to the static files for ${local.app_name}"
  policy      = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation",
        "s3:ListBucketMultipartUploads",
        "s3:ListBucketVersions"
      ],
      "Resource": "arn:aws:s3:::${aws_s3_bucket.static.id}"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:*Object*",
        "s3:ListMultipartUploadParts",
        "s3:AbortMultipartUpload"
      ],
      "Resource": "arn:aws:s3:::${aws_s3_bucket.static.id}/*"
    }
  ]
}
EOF
}


// Security Groups

resource "aws_security_group" "db" {
  ingress {
    protocol        = "tcp"
    from_port       = 5432
    to_port         = 5432
    security_groups = ["${aws_security_group.web.id}"]
    description     = "Allow access from webservers"
  }

  tags {
    Application = "${local.app_name}"
    Name        = "${local.app_name} Databases"
  }
}

resource "aws_security_group" "web" {
  name_prefix = "${local.app_name}"

  # Allow incoming HTTP connections from anywhere
  ingress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP traffic from anywhere"
  }

  # Allow incoming HTTPS connections from anywhere
  ingress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS traffic from anywhere"
  }

  # Allow incoming SSH connections from anywhere
  ingress {
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH traffic from anywhere"
  }

  # Allow any outogoing traffic. This is necessary for things like software
  # updates.
  egress {
    protocol    = -1
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outgoing traffic"
  }

  tags {
    Application = "${local.app_name}"
    Name        = "${local.app_name} Webservers"
  }
}


// Set up Route 53 records

resource "aws_route53_record" "web" {
  name    = "${local.sub_domain}"
  records = ["${aws_instance.webserver.public_ip}"]
  ttl     = 60
  type    = "A"
  zone_id = "${data.aws_route53_zone.main.zone_id}"
}
