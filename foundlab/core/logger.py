import os
import json
from google.cloud import pubsub_v1
from foundlab.core.veritas import VeritasEvent

# --- Configuração ---
# Estes valores devem corresponder ao que está definido no Terraform.
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "seu-gcp-project-id-aqui")
TOPIC_ID = "veritas-reputation-updates"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(GCP_PROJECT_ID, TOPIC_ID)

def publish_event(event: VeritasEvent):
    """
    Publica um VeritasEvent no tópico do Google Cloud Pub/Sub.

    Args:
        event: O objeto VeritasEvent a ser publicado.
    
    Raises:
        Exception: Se a publicação falhar.
    """
    try:
        # Serializa o evento para uma string JSON
        event_data = json.dumps(event.to_dict()).encode("utf-8")

        # Publica a mensagem
        future = publisher.publish(topic_path, event_data)
        
        # Espera a confirmação da publicação
        message_id = future.result()
        print(f"Evento {event.eventType} ({event.decisionId}) publicado com sucesso. Message ID: {message_id}")

    except Exception as e:
        print(f"Erro ao publicar o evento {event.decisionId}: {e}")
        raise
