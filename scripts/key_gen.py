from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

private_key = ed25519.Ed25519PrivateKey.generate()

with open('private_key', 'wb') as f:
    private_key_bytes = private_key.private_bytes(encoding=serialization.Encoding.PEM, 
                                      format=serialization.PrivateFormat.PKCS8,
                                      encryption_algorithm=serialization.NoEncryption())
    f.write(private_key_bytes)

with open('public_key', 'wb') as f:
    public_key_bytes = private_key.public_key().public_bytes(encoding=serialization.Encoding.OpenSSH,
                                                             format=serialization.PublicFormat.OpenSSH)
    f.write(public_key_bytes)