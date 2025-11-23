#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test para verificar guardado en BD
"""

from jwt_analyzer.mongodb import TokenRepository, mongo

# Verificar conexión
print("Conectado:", mongo.is_connected())

if mongo.is_connected():
    print("\nÚltimos 5 tokens en BD:")
    tokens = TokenRepository.get_all_tokens(limit=5)
    for i, token in enumerate(tokens, 1):
        print(f"{i}. Token: {str(token.get('token', ''))[:50]}...")
        print(f"   Tipo: {token.get('type')}")
        print(f"   Algoritmo: {token.get('algorithm')}")
        print(f"   Creado: {token.get('created_at')}")
        print()

    # Intentar buscar un token específico
    print("\nBuscando token en BD...")
    # Token de prueba
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    result = TokenRepository.get_token_by_token_string(test_token)
    if result:
        print(f"[OK] Token encontrado en BD")
        print(f"   ID: {result.get('_id')}")
    else:
        print("[INFO] Token no encontrado en BD (probablemente es la primera vez)")
else:
    print("[ERROR] MongoDB no está conectado")
