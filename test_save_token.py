#!/usr/bin/env python3
"""
Script de prueba para verificar si se guardan los tokens en MongoDB
"""

from jwt_analyzer.mongodb import mongo, TokenRepository
from datetime import datetime
import json

print("=" * 70)
print("TEST: Guardar Token en MongoDB")
print("=" * 70)

# Conectar
print("\n1. Conectando a MongoDB...")
mongo.connect()

if not mongo.is_connected():
    print("❌ NO CONECTADO")
    exit(1)

print("✅ Conectado a MongoDB")

# Crear datos de prueba
print("\n2. Creando token de prueba...")
test_token_data = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
    "header": {"alg": "HS256", "typ": "JWT"},
    "payload": {"sub": "1234567890", "name": "John Doe"},
    "signature": "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
    "type": "valid",
    "is_valid": True,
    "signature_valid": True,
    "algorithm": "HS256",
    "analysis": {
        "lexical": {"ok": True},
        "syntactic": {"ok": True},
        "semantic": {"ok": True}
    },
    "notes": "Token de prueba"
}

# Guardar
print("\n3. Guardando token en MongoDB...")
try:
    token_id = TokenRepository.save_token(test_token_data)
    print(f"✅ Token guardado exitosamente")
    print(f"   ID: {token_id}")
except Exception as e:
    print(f"❌ Error guardando: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Verificar
print("\n4. Verificando que se guardó...")
try:
    all_tokens = TokenRepository.get_all_tokens()
    print(f"✅ Total de tokens en DB: {len(all_tokens)}")
    
    if all_tokens:
        print(f"\n   Último token guardado:")
        token = all_tokens[0]
        print(f"   - ID: {token['_id']}")
        print(f"   - Tipo: {token['type']}")
        print(f"   - Válido: {token['is_valid']}")
        print(f"   - Algoritmo: {token['algorithm']}")
        print(f"   - Creado: {token.get('created_at', 'N/A')}")
except Exception as e:
    print(f"❌ Error verificando: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Ver estadísticas
print("\n5. Estadísticas:")
try:
    stats = TokenRepository.get_statistics()
    print(f"   Total: {stats.get('total', 0)}")
    print(f"   Válidos: {stats.get('valid', 0)}")
    print(f"   Inválidos: {stats.get('invalid', 0)}")
    print(f"   Expirados: {stats.get('expired', 0)}")
except Exception as e:
    print(f"❌ Error en estadísticas: {e}")

print("\n" + "=" * 70)
print("✅ TEST COMPLETADO")
print("=" * 70)
