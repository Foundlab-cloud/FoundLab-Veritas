import typer
from foundlab.core import crypto, veritas, logger
import os
import json
import base64
import sys
import hashlib

app = typer.Typer()

@app.command()
def sign(signer_name: str, file_path: str):
    """Signs a file and generates and publishes a Veritas Protocol event."""
    try:
        with open(file_path, "rb") as f:
            data_to_sign = f.read()
        
        # 1. Assinar os dados
        signature = crypto.sign_data(signer_name, data_to_sign)
        
        # 2. Gerar um DecisionID para esta operação
        decision_id = veritas.generate_decision_id()

        # 3. Criar o payload do evento Veritas
        payload = {
            "file_name": os.path.basename(file_path),
            "signer_name": signer_name,
            "file_content_sha256": hashlib.sha256(data_to_sign).hexdigest(),
        }

        # 4. Criar os metadados com a assinatura
        meta = {
            "signature_base64": base64.b64encode(signature).decode('utf-8'),
            "algorithm": "RSA-PSS-SHA256"
        }

        # 5. Criar o evento Veritas (genesis)
        event = veritas.create_genesis_event(
            decisionId=decision_id,
            eventType="DOCUMENT_SIGNED",
            payload=payload,
            meta=meta
        )

        # 6. Publicar o evento no Pub/Sub
        logger.publish_event(event)

        # 7. Imprimir o evento JSON no console para feedback
        print("\n--- Evento Gerado e Publicado ---")
        print(json.dumps(event.to_dict(), indent=2))
        
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

@app.command()
def verify(signer_name: str, file_path: str, signature_path: str):
    """Verifies a file's signature."""
    try:
        with open(file_path, "rb") as f:
            data_to_verify = f.read()
            
        with open(signature_path, "rb") as f:
            signature = f.read()
            
        is_valid = crypto.verify_signature(signer_name, signature, data_to_verify)
        
        if is_valid:
            print("Signature is valid.")
        else:
            print("Signature is invalid.")
            
    except FileNotFoundError:
        print(f"Error: File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    app()
