import base64
from typing import Tuple

def b64url_encode(data: bytes) -> str:
    """Encode bytes to Base64URL without padding."""
    s = base64.urlsafe_b64encode(data).decode('utf-8')
    return s.rstrip('=')

def b64url_decode(s: str) -> bytes:
    """Decode Base64URL string (handles missing padding)."""
    if not isinstance(s, str):
        raise TypeError("Input must be str")
    # Add required padding
    rem = len(s) % 4
    if rem:
        s += '=' * (4 - rem)
    try:
        return base64.urlsafe_b64decode(s.encode('utf-8'))
    except Exception as e:
        raise ValueError(f"Invalid Base64URL input: {e}")
