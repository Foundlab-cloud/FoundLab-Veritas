terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }

  backend "gcs" {
    bucket = "foundlab-veritas-tfstate" # !!! ATENÇÃO: Crie este bucket manualmente !!!
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_storage_bucket" "foundlab_artifacts" {
  name          = "foundlab-veritas-artifacts"
  location      = var.gcp_region
  force_destroy = true
}

resource "google_bigquery_dataset" "audit" {
  dataset_id = "audit"
  location   = var.gcp_region
}

resource "google_bigquery_table" "veritas_audit_trail" {
  dataset_id = google_bigquery_dataset.audit.dataset_id
  table_id   = "Veritas_Audit_Trail"
  project    = var.gcp_project_id
  location   = var.gcp_region

  time_partitioning {
    type  = "DAY"
    field = "timestamp"
  }

  clustering = ["decisionId", "eventType"]

  schema = <<EOF
[
  {
    "name": "decisionId",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "timestamp",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  },
  {
    "name": "eventType",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "payloadHash",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "previousChainHash",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "chainHash",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "meta",
    "type": "JSON",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_pubsub_topic" "reputation_updates" {
  name = "veritas-reputation-updates"
}

# --- Service Account para a Cloud Function ---

resource "google_service_account" "veritas_function_sa" {
  account_id   = "veritas-function-sa"
  display_name = "Veritas Cloud Function Service Account"
}

resource "google_project_iam_member" "secret_accessor" {
  project = var.gcp_project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.veritas_function_sa.email}"
}

resource "google_project_iam_member" "pubsub_publisher" {
  project = var.gcp_project_id
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.veritas_function_sa.email}"
}

resource "google_project_iam_member" "bigquery_editor" {
  project = var.gcp_project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.veritas_function_sa.email}"
}

output "bucket_name" {
  value = google_storage_bucket.foundlab_artifacts.name
}

output "function_service_account_email" {
  value = google_service_account.veritas_function_sa.email
}
