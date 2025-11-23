# encoder.py
import json
from .base64url import b64url_encode
from .crypto_verify import sign_hmac
from typing import Dict

def encode_jwt(header: Dict, payload: Dict, secret: bytes) -> str:
    # Ensure header/payload are dictionaries
    h_json = json.dumps(header, separators=(',', ':'), sort_keys=True).encode('utf-8')
    p_json = json.dumps(payload, separators=(',', ':'), sort_keys=True).encode('utf-8')
    h_b64 = b64url_encode(h_json)
    p_b64 = b64url_encode(p_json)
    alg = header.get("alg")
    signing_input = f"{h_b64}.{p_b64}".encode('utf-8')
    signature = sign_hmac(signing_input, secret, alg)
    signature_b64 = b64url_encode(signature)
    return f"{h_b64}.{p_b64}.{signature_b64}"
