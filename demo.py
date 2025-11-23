#!/usr/bin/env python3
"""
Script de demostración del JWT Analyzer
Muestra todas las funcionalidades del analizador
"""

import json
import time
from jwt_analyzer.encoder import encode_jwt
from jwt_analyzer.parser import JWTParser
from jwt_analyzer.semantic import validate_header, validate_payload
from jwt_analyzer.crypto_verify import verify_signature
from jwt_analyzer.lexer import LexerJWT
from jwt_analyzer.base64url import b64url_encode

print("=" * 80)
print("JWT ANALYZER - DEMOSTRACIÓN COMPLETA")
print("=" * 80)

# DEMO 1: Crear un token válido
print("\n[DEMO 1] Crear un token JWT válido con HS256")
print("-" * 80)

header = {"alg": "HS256", "typ": "JWT"}
payload = {
    "sub": "1234567890",
    "name": "John Doe",
    "email": "john.doe@example.com",
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600  # Válido por 1 hora
}
secret = b"mysecretkey"

token = encode_jwt(header, payload, secret)
print(f"Token creado:\n{token}\n")

# Mostrar las partes
parts = token.split('.')
print(f"Estructura del token:")
print(f"  HEADER:    {parts[0]}")
print(f"  PAYLOAD:   {parts[1]}")
print(f"  SIGNATURE: {parts[2]}")

# DEMO 2: Análisis Léxico
print("\n[DEMO 2] Análisis Léxico")
print("-" * 80)

lexer = LexerJWT()
tokens = lexer.tokenize(token)
print("Tokens detectados:")
for t in tokens:
    print(f"  {t.type}: {t.value[:30]}... (longitud: {len(t.value)})")

# DEMO 3: Análisis Sintáctico y Semántico
print("\n[DEMO 3] Análisis Sintáctico y Semántico")
print("-" * 80)

parser = JWTParser()
parsed = parser.parse(token)

print("Header decodificado:")
print(json.dumps(parsed["header"], indent=2))

print("\nPayload decodificado:")
print(json.dumps(parsed["payload"], indent=2))

# Validar header
try:
    validate_header(parsed["header"])
    print("\n✓ Header válido")
except Exception as e:
    print(f"\n✗ Header inválido: {e}")

# Validar payload
try:
    validate_payload(parsed["payload"], check_time=False)
    print("✓ Payload válido")
except Exception as e:
    print(f"✗ Payload inválido: {e}")

# DEMO 4: Verificación de firma
print("\n[DEMO 4] Verificación de Firma")
print("-" * 80)

# Con secret correcto
is_valid = verify_signature(
    parsed["header_b64"],
    parsed["payload_b64"],
    parsed["signature"],
    secret,
    "HS256"
)
print(f"✓ Firma verificada con secret correcto: {is_valid}")

# Con secret incorrecto
wrong_secret = b"wrongsecret"
is_valid_wrong = verify_signature(
    parsed["header_b64"],
    parsed["payload_b64"],
    parsed["signature"],
    wrong_secret,
    "HS256"
)
print(f"✓ Firma verificada con secret incorrecto: {is_valid_wrong}")

# DEMO 5: Token expirado
print("\n[DEMO 5] Token Expirado")
print("-" * 80)

expired_payload = {
    "sub": "user123",
    "iat": 1600000000,
    "exp": 1600000001  # Expirado hace mucho tiempo
}

expired_token = encode_jwt(header, expired_payload, secret)
print(f"Token expirado creado")

parsed_expired = parser.parse(expired_token)

try:
    validate_payload(parsed_expired["payload"], check_time=True)
    print("✓ Token aún válido")
except Exception as e:
    print(f"✗ Token expirado: {e}")

# DEMO 6: Token con firma alterada
print("\n[DEMO 6] Token con Firma Alterada")
print("-" * 80)

parts = token.split('.')
# Cambiar un carácter en la firma
tampered_signature = parts[2][:-1] + ('A' if parts[2][-1] != 'A' else 'B')
tampered_token = f"{parts[0]}.{parts[1]}.{tampered_signature}"

print(f"Token original:  {token[:50]}...")
print(f"Token alterado:  {tampered_token[:50]}...")

parsed_tampered = parser.parse(tampered_token)

is_valid_tampered = verify_signature(
    parsed_tampered["header_b64"],
    parsed_tampered["payload_b64"],
    parsed_tampered["signature"],
    secret,
    "HS256"
)

print(f"Firma del token alterado: {is_valid_tampered}")

# DEMO 7: Token con HS384
print("\n[DEMO 7] Token con Algoritmo HS384")
print("-" * 80)

header_hs384 = {"alg": "HS384", "typ": "JWT"}
token_hs384 = encode_jwt(header_hs384, payload, secret)
print(f"Token HS384 creado:\n{token_hs384}\n")

parsed_hs384 = parser.parse(token_hs384)

is_valid_hs384 = verify_signature(
    parsed_hs384["header_b64"],
    parsed_hs384["payload_b64"],
    parsed_hs384["signature"],
    secret,
    "HS384"
)

print(f"✓ Firma HS384 válida: {is_valid_hs384}")

# Comparar tamaño de firmas
sig_hs256 = token.split('.')[-1]
sig_hs384 = token_hs384.split('.')[-1]
print(f"Longitud firma HS256: {len(sig_hs256)} caracteres")
print(f"Longitud firma HS384: {len(sig_hs384)} caracteres")

# DEMO 8: Resumen de funcionalidades
print("\n" + "=" * 80)
print("RESUMEN DE FUNCIONALIDADES DEMOSTRADAS")
print("=" * 80)

features = [
    "✓ Análisis Léxico: Tokenización en 3 partes",
    "✓ Análisis Sintáctico: Validación de estructura gramatical",
    "✓ Análisis Semántico: Validación de campos obligatorios y tipos",
    "✓ Decodificación: Base64URL y JSON",
    "✓ Verificación de Firma: HMAC con HS256 y HS384",
    "✓ Validación Temporal: Claims exp, iat, nbf",
    "✓ Detección de Manipulaciones: Compare digest para timing-safe",
    "✓ Creación de Tokens: Con firma criptográfica",
]

for feature in features:
    print(feature)

print("\n" + "=" * 80)
print("Demostración completada exitosamente")
print("=" * 80)
