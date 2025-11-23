# parser.py
from typing import Dict, Any
import json
from .lexer import LexerJWT, LexerError
from .base64url import b64url_decode

class ParserError(Exception):
    pass

class JWTParser:
    def __init__(self):
        self.lexer = LexerJWT()

    def parse(self, jwt_string: str) -> Dict[str, Any]:
        """
        Returns dict: {
          "header_b64": str,
          "payload_b64": str,
          "signature_b64": str,
          "header": dict,
          "payload": dict,
          "signature": bytes
        }
        """
        tokens = self.lexer.tokenize(jwt_string)
        h_b64 = tokens[0].value
        p_b64 = tokens[1].value
        s_b64 = tokens[2].value

        try:
            header_bytes = b64url_decode(h_b64)
            payload_bytes = b64url_decode(p_b64)
            signature_bytes = b64url_decode(s_b64)
        except Exception as e:
            raise ParserError(f"Base64URL decoding error: {e}")

        try:
            header = json.loads(header_bytes.decode('utf-8'))
        except Exception as e:
            raise ParserError(f"Header is not valid JSON: {e}")
        try:
            payload = json.loads(payload_bytes.decode('utf-8'))
        except Exception as e:
            raise ParserError(f"Payload is not valid JSON: {e}")

        return {
            "header_b64": h_b64,
            "payload_b64": p_b64,
            "signature_b64": s_b64,
            "header": header,
            "payload": payload,
            "signature": signature_bytes
        }
