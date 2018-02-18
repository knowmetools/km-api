// Generic AWS Configuration

variable "aws_region" {
  default     = "us-east-1"
  description = "The AWS region to deploy to."
  type        = "string"
}

// Database Configuration

variable "db_capacity" {
  default     = 5
  description = "Capacity of the database in GB."
  type        = "string"
}

variable "db_instance_type" {
  default     = "db.t2.micro"
  description = "The instance type to use for the database."
  type        = "string"
}

variable "db_master_username" {
  description = "The username for the database's admin account."
  type        = "string"
}

variable "db_master_password" {
  description = "The password for the database's admin account."
  type        = "string"
}


// Webserver Configuration

variable "web_instance_type" {
  default     = "t2.nano"
  description = "The instance type of the webserver."
  type        = "string"
}

variable "public_key_path" {
  default     = "~/.ssh/id_rsa.pub"
  description = "The path to the public key used to SSH into the webserver."
  type        = "string"
}

variable "route53_zone_name" {
  default     = "knowmetools.com."
  description = "The name of the Route 53 zone the webserver's record is created in."
  type        = "string"
}
