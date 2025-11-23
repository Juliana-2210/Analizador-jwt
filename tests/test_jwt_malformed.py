import pytest
from jwt_analyzer.lexer import LexerJWT, LexerError

def test_missing_parts():
    lexer = LexerJWT()
    with pytest.raises(LexerError):
        lexer.tokenize("abc.def")  # solo 2 partes

def test_invalid_characters():
    lexer = LexerJWT()
    # incluir carácter no permitido en base64url
    with pytest.raises(LexerError):
        lexer.tokenize("a*b.c.d")
