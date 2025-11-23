# semantic.py
import time
from typing import Dict, Any

class SemanticError(Exception):
    pass

REQUIRED_HEADER_FIELDS = ["alg", "typ"]
REQUIRED_PAYLOAD_FIELDS = []  # not all payload claims are required globally; enforce some standards below

STANDARD_CLAIMS = ["iss", "sub", "exp", "iat", "nbf", "aud", "jti"]

def validate_header(header: Dict[str,Any]):
    if not isinstance(header, dict):
        raise SemanticError("Header must be an object")
    for f in REQUIRED_HEADER_FIELDS:
        if f not in header:
            raise SemanticError(f"Missing header field: {f}")
    # typ must be "JWT"
    if header.get("typ") != "JWT":
        raise SemanticError(f'Header.typ must be "JWT" (found: {header.get("typ")})')
    if not isinstance(header.get("alg"), str):
        raise SemanticError("Header.alg must be a string")
    # recognize only HS256 or HS384 for this project
    if header.get("alg") not in ("HS256", "HS384"):
        raise SemanticError("Unsupported alg. Only HS256 and HS384 are allowed in this implementation")

def validate_payload(payload: Dict[str,Any], check_time: bool=True):
    if not isinstance(payload, dict):
        raise SemanticError("Payload must be an object")
    # Validate types for common temporal claims if present
    for claim in ("exp","iat","nbf"):
        if claim in payload:
            if not isinstance(payload[claim], (int, float)):
                raise SemanticError(f"Claim {claim} must be a numeric timestamp (int)")

    # expiration check
    if check_time and "exp" in payload:
        now = int(time.time())
        if int(payload["exp"]) < now:
            raise SemanticError("Token has expired (exp claim)")
