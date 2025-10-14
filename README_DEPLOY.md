# ☁ FoundLab Veritas Cloud Nexus (GCP Edition)

Deploy automático do framework FoundLab na infraestrutura do Google Cloud.

## Passos
⿡ Autenticação:
   gcloud auth application-default login

⿢ Inicialização:
   python gcp/init_bigquery.py
   python gcp/init_pubsub.py

⿣ Deploy da Cloud Function:
   bash gcp/deploy_gcp.sh
