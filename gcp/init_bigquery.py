import os
from google.cloud import bigquery

# Get project ID from environment variable
project = os.environ.get("GOOGLE_CLOUD_PROJECT")
if not project:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

client = bigquery.Client(project=project)
dataset_id = f"{project}.veritas_audit"

dataset_ref = bigquery.Dataset(f"{project}.{dataset_id}")
dataset_ref.location = "southamerica-east1"
client.create_dataset(dataset_ref, exists_ok=True)

schema = [
    bigquery.SchemaField("decision_id", "STRING"),
    bigquery.SchemaField("artifact", "STRING"),
    bigquery.SchemaField("hash", "STRING"),
    bigquery.SchemaField("timestamp", "TIMESTAMP"),
    bigquery.SchemaField("sdid", "STRING"),
    bigquery.SchemaField("metadata", "STRING"),
]
table_ref = client.dataset(dataset_id).table("veritas_ledger")
table = bigquery.Table(table_ref, schema=schema)
client.create_table(table, exists_ok=True)
print("✅ BigQuery inicializado.")
