"""Test JWT con diferentes algoritmos (HS256, HS384)."""
import pytest
from jwt_analyzer.encoder import encode_jwt
from jwt_analyzer.parser import JWTParser
from jwt_analyzer.semantic import validate_header, validate_payload
from jwt_analyzer.crypto_verify import verify_signature
from jwt_analyzer.utils import make_standard_header, now_ts


def test_hs256_algorithm(secret):
    """Validar que HS256 funciona correctamente."""
    header = make_standard_header("HS256")
    payload = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": now_ts(),
        "exp": now_ts() + 3600
    }
    
    token = encode_jwt(header, payload, secret)
    
    p = JWTParser()
    parsed = p.parse(token)
    
    # Validar header y payload
    validate_header(parsed["header"])
    validate_payload(parsed["payload"])
    
    # Validar que algoritmo es HS256
    assert parsed["header"]["alg"] == "HS256"
    
    # Verificar firma
    ok = verify_signature(
        parsed["header_b64"],
        parsed["payload_b64"],
        parsed["signature"],
        secret,
        "HS256"
    )
    assert ok


def test_hs384_algorithm(secret):
    """Validar que HS384 funciona correctamente."""
    header = {
        "alg": "HS384",
        "typ": "JWT"
    }
    payload = {
        "sub": "1234567890",
        "name": "Jane Doe",
        "iat": now_ts(),
        "exp": now_ts() + 3600
    }
    
    token = encode_jwt(header, payload, secret)
    
    p = JWTParser()
    parsed = p.parse(token)
    
    # Validar header y payload
    validate_header(parsed["header"])
    validate_payload(parsed["payload"])
    
    # Validar que algoritmo es HS384
    assert parsed["header"]["alg"] == "HS384"
    
    # Verificar firma
    ok = verify_signature(
        parsed["header_b64"],
        parsed["payload_b64"],
        parsed["signature"],
        secret,
        "HS384"
    )
    assert ok


def test_hs256_and_hs384_different_signatures(secret):
    """Verificar que HS256 y HS384 producen diferentes firmas."""
    payload = {
        "sub": "1234567890",
        "iat": now_ts(),
        "exp": now_ts() + 3600
    }
    
    header_hs256 = make_standard_header("HS256")
    token_hs256 = encode_jwt(header_hs256, payload, secret)
    
    header_hs384 = {"alg": "HS384", "typ": "JWT"}
    token_hs384 = encode_jwt(header_hs384, payload, secret)
    
    # Tokens deben ser diferentes
    assert token_hs256 != token_hs384
    
    # Las firmas (última parte) deben ser diferentes
    sig_hs256 = token_hs256.split(".")[-1]
    sig_hs384 = token_hs384.split(".")[-1]
    assert sig_hs256 != sig_hs384


def test_hs384_signature_longer_than_hs256(secret):
    """HS384 produce firmas más largas que HS256."""
    payload = {
        "sub": "1234567890",
        "iat": now_ts(),
        "exp": now_ts() + 3600
    }
    
    header_hs256 = make_standard_header("HS256")
    token_hs256 = encode_jwt(header_hs256, payload, secret)
    
    header_hs384 = {"alg": "HS384", "typ": "JWT"}
    token_hs384 = encode_jwt(header_hs384, payload, secret)
    
    # Extraer firmas (Base64URL encoded)
    sig_hs256 = token_hs256.split(".")[-1]
    sig_hs384 = token_hs384.split(".")[-1]
    
    # HS384 produce SHA384 (48 bytes) vs HS256 SHA256 (32 bytes)
    # Cuando se codifican en base64, HS384 será más largo
    assert len(sig_hs384) >= len(sig_hs256)


def test_hs256_wrong_secret_fails_verification(secret):
    """Verificación de firma falla con secret incorrecto en HS256."""
    header = make_standard_header("HS256")
    payload = {
        "sub": "1234567890",
        "iat": now_ts(),
        "exp": now_ts() + 3600
    }
    
    token = encode_jwt(header, payload, secret)
    
    p = JWTParser()
    parsed = p.parse(token)
    
    wrong_secret = b"wrongsecret"
    ok = verify_signature(
        parsed["header_b64"],
        parsed["payload_b64"],
        parsed["signature"],
        wrong_secret,
        "HS256"
    )
    assert not ok


def test_hs384_wrong_secret_fails_verification(secret):
    """Verificación de firma falla con secret incorrecto en HS384."""
    header = {
        "alg": "HS384",
        "typ": "JWT"
    }
    payload = {
        "sub": "1234567890",
        "iat": now_ts(),
        "exp": now_ts() + 3600
    }
    
    token = encode_jwt(header, payload, secret)
    
    p = JWTParser()
    parsed = p.parse(token)
    
    wrong_secret = b"wrongsecret"
    ok = verify_signature(
        parsed["header_b64"],
        parsed["payload_b64"],
        parsed["signature"],
        wrong_secret,
        "HS384"
    )
    assert not ok


def test_hs256_with_longer_secret(secret):
    """HS256 debe funcionar con secrets de diferentes longitudes."""
    long_secret = b"this_is_a_very_long_secret_key_with_many_characters_123456789"
    
    header = make_standard_header("HS256")
    payload = {
        "sub": "1234567890",
        "iat": now_ts(),
        "exp": now_ts() + 3600
    }
    
    token = encode_jwt(header, payload, long_secret)
    
    p = JWTParser()
    parsed = p.parse(token)
    
    # Verificar con el mismo secret largo
    ok = verify_signature(
        parsed["header_b64"],
        parsed["payload_b64"],
        parsed["signature"],
        long_secret,
        "HS256"
    )
    assert ok
