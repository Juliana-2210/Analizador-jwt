"""Test JWT con campos requeridos faltantes."""
import pytest
import json
from jwt_analyzer.encoder import encode_jwt
from jwt_analyzer.parser import JWTParser
from jwt_analyzer.semantic import validate_header, validate_payload, SemanticError
from jwt_analyzer.base64url import b64url_encode
from jwt_analyzer.crypto_verify import sign_hmac
from jwt_analyzer.utils import make_standard_header, now_ts


def test_header_missing_alg(secret):
    """Header debe tener field 'alg'."""
    # Crear header sin alg manualmente
    header = {"typ": "JWT"}  # falta alg
    
    with pytest.raises(SemanticError) as exc_info:
        validate_header(header)
    assert "alg" in str(exc_info.value).lower()


def test_header_missing_typ(secret):
    """Header debe tener field 'typ'."""
    header = {"alg": "HS256"}  # falta typ
    
    with pytest.raises(SemanticError) as exc_info:
        validate_header(header)
    assert "typ" in str(exc_info.value).lower()


def test_header_missing_both(secret):
    """Header debe tener ambos: 'alg' y 'typ'."""
    header = {}  # vacío
    
    with pytest.raises(SemanticError) as exc_info:
        validate_header(header)
    # Debe faltar al menos uno
    error_msg = str(exc_info.value).lower()
    assert "alg" in error_msg or "typ" in error_msg


def test_payload_wrong_type_in_sub(secret):
    """Validar que payload sea dict, no string o número."""
    # Intentar con payload como string en validación
    with pytest.raises(SemanticError) as exc_info:
        validate_payload("not a dict", check_time=False)
    assert "object" in str(exc_info.value).lower()


def test_header_unsupported_algorithm(secret):
    """Solo HS256 y HS384 son soportados."""
    header = {
        "alg": "RS256",  # no soportado
        "typ": "JWT"
    }
    
    with pytest.raises(SemanticError) as exc_info:
        validate_header(header)
    assert "alg" in str(exc_info.value).lower() or "unsupported" in str(exc_info.value).lower()


def test_payload_as_array_not_dict(secret):
    """Payload debe ser un objeto (dict), no array."""
    payload_array = ["claim1", "claim2"]
    
    with pytest.raises(SemanticError) as exc_info:
        validate_payload(payload_array, check_time=False)
    assert "object" in str(exc_info.value).lower()


def test_payload_as_string_not_dict(secret):
    """Payload debe ser un objeto (dict), no string."""
    payload_string = "invalid payload"
    
    with pytest.raises(SemanticError) as exc_info:
        validate_payload(payload_string, check_time=False)
    assert "object" in str(exc_info.value).lower()


def test_payload_as_null_not_dict(secret):
    """Payload debe ser un objeto (dict), no null."""
    payload_none = None
    
    with pytest.raises(SemanticError) as exc_info:
        validate_payload(payload_none, check_time=False)
    assert "object" in str(exc_info.value).lower()


def test_header_as_not_dict(secret):
    """Header debe ser un objeto (dict)."""
    from jwt_analyzer.semantic import validate_header
    
    header_array = ["alg", "HS256"]
    
    with pytest.raises(SemanticError) as exc_info:
        validate_header(header_array)
    assert "object" in str(exc_info.value).lower()
