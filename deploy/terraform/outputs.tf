output "database" {
  description = "The endpoint used to connect to the database."
  value       = "${aws_db_instance.main.address}"
}

output "static_bucket" {
  description = "The S3 bucket used to store static files."
  value       = "${aws_s3_bucket.static.id}"
}

output "webserver" {
  description = "The FQDN of the webserver."
  value       = "${aws_route53_record.web.fqdn}"
}
