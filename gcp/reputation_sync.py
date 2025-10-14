import base64
import json
from google.cloud import bigquery

# --- Configuração ---
# O ID do projeto é inferido automaticamente do ambiente da Cloud Function.
BIGQUERY_DATASET = "audit"
BIGQUERY_TABLE = "Veritas_Audit_Trail"

client = bigquery.Client() # O projeto é inferido do ambiente

def sync_reputation(event, context):
    """
    Cloud Function acionada por uma mensagem no Pub/Sub.
    Recebe um VeritasEvent e o insere na tabela de auditoria do BigQuery.
    """
    # Construir o table_id dinamicamente
    table_id = f"{client.project}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"
    
    print(f"Processando evento: {context.event_id} para a tabela {table_id}")

    try:
        # 1. Decodificar a mensagem do Pub/Sub
        if 'data' in event:
            message_data = base64.b64decode(event['data']).decode('utf-8')
            event_json = json.loads(message_data)
            print(f"Evento decodificado: {event_json}")
        else:
            raise ValueError("A mensagem do Pub/Sub não contém o campo 'data'.")

        # 2. Validar o evento (verificação mínima)
        required_keys = ["decisionId", "timestamp", "eventType", "payloadHash", "chainHash"]
        if not all(key in event_json for key in required_keys):
            raise ValueError(f"O evento JSON não contém todas as chaves obrigatórias. Recebido: {event_json.keys()}")

        # 3. Inserir a linha no BigQuery
        # O BigQuery Client lida com a correspondência de campos do dicionário para as colunas da tabela.
        errors = client.insert_rows_json(table_id, [event_json])

        if errors == []:
            print(f"Evento {event_json['decisionId']} inserido com sucesso no BigQuery.")
        else:
            print(f"Erro ao inserir evento no BigQuery: {errors}")
            # Você pode adicionar lógica de tratamento de erro aqui (ex: enviar para uma DLQ)

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except ValueError as e:
        print(f"Erro de valor: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

