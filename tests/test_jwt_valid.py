from jwt_analyzer.parser import JWTParser
from jwt_analyzer.semantic import validate_header, validate_payload
from jwt_analyzer.crypto_verify import verify_signature

def test_valid_token(valid_token, secret):
    p = JWTParser()
    parsed = p.parse(valid_token)

    # Validar sintaxis semántica
    validate_header(parsed["header"])
    validate_payload(parsed["payload"])

    # Verificar firma
    ok = verify_signature(
        parsed["header_b64"],
        parsed["payload_b64"],
        parsed["signature"],
        secret,
        parsed["header"]["alg"]
    )
    assert ok
