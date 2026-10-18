locals {
  layers = toset(["landing", "bronze"])
}

resource "aws_s3_bucket" "layer" {
  for_each = local.layers
  bucket   = "${var.project}-${each.key}"
}

resource "aws_s3_bucket_versioning" "layer" {
  for_each = local.layers
  bucket   = aws_s3_bucket.layer[each.key].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "layer" {
  for_each                = local.layers
  bucket                  = aws_s3_bucket.layer[each.key].id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "layer" {
  for_each = local.layers
  bucket   = aws_s3_bucket.layer[each.key].id
  rule {
    bucket_key_enabled = true
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}