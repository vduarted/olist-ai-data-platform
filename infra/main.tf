resource "aws_s3_bucket" "bronze" {
  bucket = "olist-bronze"

  tags = {
    env = "dev"
  }
}