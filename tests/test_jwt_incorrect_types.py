"""Test JWT con tipos de datos incorrectos en claims."""
import pytest
from jwt_analyzer.encoder import encode_jwt
from jwt_analyzer.parser import JWTParser
from jwt_analyzer.semantic import validate_payload, SemanticError
from jwt_analyzer.utils import make_standard_header, now_ts


def test_exp_claim_as_string(secret):
    """La claim 'exp' debe ser número, no string."""
    header = make_standard_header("HS256")
    payload = {
        "sub": "1234567890",
        "iat": now_ts(),
        "exp": "not_a_number"  # ERROR: debería ser int
    }
    token = encode_jwt(header, payload, secret)
    
    p = JWTParser()
    parsed = p.parse(token)
    
    with pytest.raises(SemanticError) as exc_info:
        validate_payload(parsed["payload"], check_time=False)
    assert "exp" in str(exc_info.value)
    assert "numeric" in str(exc_info.value).lower()


def test_iat_claim_as_string(secret):
    """La claim 'iat' debe ser número, no string."""
    header = make_standard_header("HS256")
    payload = {
        "sub": "1234567890",
        "iat": "not_a_number",  # ERROR: debería ser int
        "exp": now_ts() + 3600
    }
    token = encode_jwt(header, payload, secret)
    
    p = JWTParser()
    parsed = p.parse(token)
    
    with pytest.raises(SemanticError) as exc_info:
        validate_payload(parsed["payload"], check_time=False)
    assert "iat" in str(exc_info.value)
    assert "numeric" in str(exc_info.value).lower()


def test_nbf_claim_as_string(secret):
    """La claim 'nbf' debe ser número, no string."""
    header = make_standard_header("HS256")
    payload = {
        "sub": "1234567890",
        "nbf": "not_a_number",  # ERROR: debería ser int
        "exp": now_ts() + 3600
    }
    token = encode_jwt(header, payload, secret)
    
    p = JWTParser()
    parsed = p.parse(token)
    
    with pytest.raises(SemanticError) as exc_info:
        validate_payload(parsed["payload"], check_time=False)
    assert "nbf" in str(exc_info.value)
    assert "numeric" in str(exc_info.value).lower()


def test_payload_not_dict(secret):
    """El payload debe ser un diccionario, no un array."""
    header = make_standard_header("HS256")
    # Intentar crear un token con payload como array
    payload = ["item1", "item2"]  # ERROR: debería ser dict
    token = encode_jwt(header, payload, secret)
    
    p = JWTParser()
    parsed = p.parse(token)
    
    with pytest.raises(SemanticError) as exc_info:
        validate_payload(parsed["payload"], check_time=False)
    assert "object" in str(exc_info.value).lower()


def test_header_typ_incorrect(secret):
    """Header.typ debe ser 'JWT', no otro valor."""
    from jwt_analyzer.semantic import validate_header
    
    header = {
        "alg": "HS256",
        "typ": "JWE"  # ERROR: debería ser JWT
    }
    payload = {
        "sub": "1234567890",
        "iat": now_ts(),
        "exp": now_ts() + 3600
    }
    token = encode_jwt(header, payload, secret)
    
    p = JWTParser()
    parsed = p.parse(token)
    
    with pytest.raises(SemanticError) as exc_info:
        validate_header(parsed["header"])
    assert "typ" in str(exc_info.value).lower()


def test_header_alg_not_string(secret):
    """Header.alg debe ser string."""
    from jwt_analyzer.semantic import validate_header
    
    # No se puede crear token con alg como int directamente,
    # pero podemos simular el error de validación
    header = {
        "alg": 256,  # ERROR: debería ser string
        "typ": "JWT"
    }
    
    with pytest.raises(SemanticError) as exc_info:
        validate_header(header)
    assert "alg" in str(exc_info.value).lower()
