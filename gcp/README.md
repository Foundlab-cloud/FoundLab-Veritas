# GCP Infrastructure Scripts

This directory contains scripts for initializing Google Cloud Platform resources required by the Veritas protocol.

## Prerequisites

Before running these scripts, ensure you have:
1. Authenticated with the Google Cloud SDK:
   ```bash
   gcloud auth application-default login
   ```
2. Set the `GOOGLE_CLOUD_PROJECT` environment variable to your target GCP project ID:
   ```bash
   # PowerShell
   $env:GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

   # Bash
   export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   ```

## Scripts

*   `init_bigquery.py`: Creates the BigQuery dataset and table required for the Veritas audit trail.
*   `init_pubsub.py`: Creates the Pub/Sub topic for reputation updates.
*   `reputation_sync.py`: A sample script demonstrating how to process events.
