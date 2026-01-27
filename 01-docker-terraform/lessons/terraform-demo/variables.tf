variable "credentials" {
  description = "My Credentails"
  default     = "./keys/service_account_key.json"
}

variable "project" {
  description = "Project"
  default     = "hale-silicon-477315-r2"
}

variable "region" {
  description = "Region"
  default     = "europe-west1"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "hale-silicon-477315-r2-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}