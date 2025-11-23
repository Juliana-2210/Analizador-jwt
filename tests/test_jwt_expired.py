import pytest
from jwt_analyzer.parser import JWTParser
from jwt_analyzer.semantic import validate_payload, SemanticError

def test_expired_token(expired_token):
    p = JWTParser()
    parsed = p.parse(expired_token)

    # Debe fallar porque la claim exp ya expiró
    with pytest.raises(SemanticError):
        validate_payload(parsed["payload"], check_time=True)
