terraform {
  backend "s3" {
    bucket = "fastapiapp-terraform-state-file-123"
    key    = "fastapiapp.tfstate"
    region = "us-east-1"
  }
}
