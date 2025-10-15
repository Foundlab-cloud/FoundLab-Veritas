# Signer Keys

In a production environment, all cryptographic keys (private and public) are managed securely via a service like Google Cloud Secret Manager. They are never stored as files within the repository.

The application logic in `foundlab/core/crypto.py` is designed to fetch private keys directly from Secret Manager at runtime, adhering to the principle of least privilege and avoiding hardcoded secrets.

Public keys may be stored here for convenience in a development setting, but for this demonstration, all key material has been removed to showcase best practices.
