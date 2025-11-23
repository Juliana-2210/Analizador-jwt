# lexer.py
from typing import List, Tuple
import re

B64URL_CHARS = re.compile(r'^[A-Za-z0-9\-_]+$')

class Token:
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class LexerError(Exception):
    pass

class LexerJWT:
    """
    Simple lexer for JWT: splits into three base64url parts.
    Produces tokens: HEADER_B64, PAYLOAD_B64, SIGNATURE_B64
    """
    def tokenize(self, jwt_string: str) -> List[Token]:
        if not isinstance(jwt_string, str):
            raise LexerError("JWT must be a string")
        parts = jwt_string.split('.')
        if len(parts) != 3:
            raise LexerError(f"JWT must have 3 parts separated by '.' - found {len(parts)}")
        header_b64, payload_b64, signature_b64 = parts
        for name, part in (("HEADER", header_b64), ("PAYLOAD", payload_b64), ("SIGNATURE", signature_b64)):
            if part == '':
                raise LexerError(f"{name} part is empty")
            if not B64URL_CHARS.match(part):
                # Allow '=' only if present (but standard JWT doesn't include padding)
                raise LexerError(f"{name} contains invalid Base64URL characters")
        return [
            Token("HEADER_B64", header_b64),
            Token("PAYLOAD_B64", payload_b64),
            Token("SIGNATURE_B64", signature_b64),
        ]
