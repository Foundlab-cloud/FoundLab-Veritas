import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization

def _get_key_path(signer_name, key_type):
    """Constructs the path to a key file."""
    base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'veritas', 'signers')
    filename = f"{signer_name}_{key_type}.pem"
    return os.path.join(base_path, filename)

from google.cloud import secretmanager

def load_private_key(signer_name: str):
    """Loads a private key for a given signer from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    
    # !!! ATENÇÃO: Adapte o 'project_id' para o seu ambiente !!!
    project_id = os.getenv("GCP_PROJECT_ID", "seu-gcp-project-id-aqui")
    secret_name = f"veritas_signer_{signer_name}_priv"
    
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    
    response = client.access_secret_version(request={"name": name})
    private_key_bytes = response.payload.data
    
    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
    )
    if not isinstance(private_key, rsa.RSAPrivateKey):
        raise TypeError(f"Expected an RSA private key, but got {type(private_key).__name__}")
    return private_key

def load_public_key(signer_name: str):
    """Loads a public key for a given signer."""
    path = _get_key_path(signer_name, 'pub')
    with open(path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise TypeError(f"Expected an RSA public key, but got {type(public_key).__name__}")
    return public_key

def sign_data(signer_name: str, data: bytes) -> bytes:
    """Signs data using the signer's private key."""
    private_key = load_private_key(signer_name)
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(signer_name: str, signature: bytes, data: bytes) -> bool:
    """Verifies a signature using the signer's public key."""
    public_key = load_public_key(signer_name)
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False
