import pytest
from jwt_analyzer.encoder import encode_jwt
from jwt_analyzer.utils import make_standard_header, now_ts

@pytest.fixture
def secret():
    return b"mysecretkey"

@pytest.fixture
def valid_token(secret):
    header = make_standard_header("HS256")
    payload = {
        "sub":"1234567890",
        "name":"John Doe",
        "iat": now_ts(),
        "exp": now_ts() + 3600
    }
    token = encode_jwt(header, payload, secret)
    return token

@pytest.fixture
def expired_token(secret):
    header = make_standard_header("HS256")
    payload = {
        "sub":"expired",
        "iat": 1600000000,
        "exp": 1600000001  # pasado
    }
    token = encode_jwt(header, payload, secret)
    return token
