from google.cloud import bigquery
client = bigquery.Client()
dataset_id = "foundlab"
project = "umbrella-producao"

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
