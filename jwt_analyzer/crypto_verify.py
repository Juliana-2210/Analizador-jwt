# crypto_verify.py
import hmac
import hashlib
from typing import Tuple

def sign_hmac(signing_input: bytes, secret: bytes, alg: str) -> bytes:
    if alg == "HS256":
        digestmod = hashlib.sha256
    elif alg == "HS384":
        digestmod = hashlib.sha384
    else:
        raise ValueError("Unsupported algorithm")
    return hmac.new(secret, signing_input, digestmod).digest()

def verify_signature(header_b64: str, payload_b64: str, signature_bytes: bytes, secret: bytes, alg: str) -> bool:
    signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    expected = sign_hmac(signing_input, secret, alg)
    # Use compare_digest to avoid timing attacks
    return hmac.compare_digest(expected, signature_bytes)
