from jwt_analyzer.parser import JWTParser
from jwt_analyzer.crypto_verify import verify_signature

def test_bad_signature(valid_token, secret):
    # alterar SOLO la firma
    parts = valid_token.split('.')
    signature = parts[2]

    # Cambiar un caracter válido sin romper Base64URL
    parts[2] = signature[:-1] + ('A' if signature[-1] != 'A' else 'B')

    tampered = '.'.join(parts)

    p = JWTParser()
    parsed = p.parse(tampered)

    ok = verify_signature(
        parsed["header_b64"],
        parsed["payload_b64"],
        parsed["signature"],
        secret,
        parsed["header"]["alg"]
    )

    assert not ok, "La firma alterada NO debería ser válida"
