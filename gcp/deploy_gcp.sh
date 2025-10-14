#!/bin/bash
set -e

# --- Obter variáveis do Terraform ---
echo "Obtendo saídas do Terraform..."
cd terraform
PROJECT_ID=$(terraform output -raw gcp_project_id)
REGION=$(terraform output -raw gcp_region)
SERVICE_ACCOUNT_EMAIL=$(terraform output -raw function_service_account_email)
cd ..

echo "Configurando o projeto GCP: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# --- Deploy da Cloud Function ---
echo "Realizando o deploy da Cloud Function 'reputation_sync'..."
gcloud functions deploy reputation_sync \
  --runtime python310 \
  --trigger-topic veritas-reputation-updates \
  --entry-point sync_reputation \
  --region $REGION \
  --service-account $SERVICE_ACCOUNT_EMAIL \
  --source .

echo "Deploy concluído com sucesso!"
