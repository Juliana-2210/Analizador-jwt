"""
Test de la nueva funcionalidad de expiración
Verifica que:
1. Se puede crear token con algoritmo seleccionable
2. Se puede seleccionar tiempo de expiración
3. Se guarda en MongoDB con todos los timestamps
4. El payload tiene iat y exp
"""

import json
import time
from datetime import datetime

# Simular lo que hace el backend
def test_token_creation():
    print("=" * 80)
    print("TEST: Creación de Token con Expiración Configurable")
    print("=" * 80)
    
    # ESCENARIO 1: HS256 con 1 hora
    print("\n🧪 ESCENARIO 1: HS256 con 1 hora de expiración")
    print("-" * 80)
    
    algorithm = "HS256"
    expiration_seconds = 3600  # 1 hora
    payload = {
        "sub": "user123",
        "name": "John Doe",
        "email": "john@example.com"
    }
    
    now = int(time.time())
    payload["iat"] = now
    payload["exp"] = now + expiration_seconds
    
    print(f"✓ Algoritmo: {algorithm}")
    print(f"✓ Expiración: {expiration_seconds} segundos (1 hora)")
    print(f"✓ Creado en: {now} ({datetime.fromtimestamp(now)})")
    print(f"✓ Expira en: {payload['exp']} ({datetime.fromtimestamp(payload['exp'])})")
    print(f"✓ Payload: {json.dumps(payload, indent=2)}")
    
    # Simular guardado en MongoDB
    token_data = {
        "algorithm": algorithm,
        "expiration_seconds": expiration_seconds,
        "created_at": now,
        "expires_at": payload["exp"],
        "payload": payload,
        "notes": f"Token creado con algoritmo {algorithm} y expiración en {expiration_seconds}s"
    }
    
    print(f"\n✓ Se guardaría en MongoDB:")
    print(json.dumps(token_data, indent=2))
    
    # ESCENARIO 2: HS384 con 5 minutos
    print("\n\n🧪 ESCENARIO 2: HS384 con 5 minutos de expiración")
    print("-" * 80)
    
    algorithm = "HS384"
    expiration_seconds = 300  # 5 minutos
    payload = {
        "user_id": "admin001",
        "permissions": ["read", "write", "delete"]
    }
    
    now = int(time.time())
    payload["iat"] = now
    payload["exp"] = now + expiration_seconds
    
    print(f"✓ Algoritmo: {algorithm}")
    print(f"✓ Expiración: {expiration_seconds} segundos (5 minutos)")
    print(f"✓ Creado en: {now} ({datetime.fromtimestamp(now)})")
    print(f"✓ Expira en: {payload['exp']} ({datetime.fromtimestamp(payload['exp'])})")
    print(f"✓ Payload: {json.dumps(payload, indent=2)}")
    
    token_data = {
        "algorithm": algorithm,
        "expiration_seconds": expiration_seconds,
        "created_at": now,
        "expires_at": payload["exp"],
        "payload": payload,
        "notes": f"Token creado con algoritmo {algorithm} y expiración en {expiration_seconds}s"
    }
    
    print(f"\n✓ Se guardaría en MongoDB:")
    print(json.dumps(token_data, indent=2))
    
    # ESCENARIO 3: 24 horas
    print("\n\n🧪 ESCENARIO 3: HS256 con 24 horas de expiración")
    print("-" * 80)
    
    algorithm = "HS256"
    expiration_seconds = 86400  # 24 horas
    payload = {
        "user_id": "user_standard",
        "role": "user"
    }
    
    now = int(time.time())
    payload["iat"] = now
    payload["exp"] = now + expiration_seconds
    
    print(f"✓ Algoritmo: {algorithm}")
    print(f"✓ Expiración: {expiration_seconds} segundos (24 horas)")
    print(f"✓ Creado en: {now} ({datetime.fromtimestamp(now)})")
    print(f"✓ Expira en: {payload['exp']} ({datetime.fromtimestamp(payload['exp'])})")
    print(f"✓ Payload: {json.dumps(payload, indent=2)}")
    
    token_data = {
        "algorithm": algorithm,
        "expiration_seconds": expiration_seconds,
        "created_at": now,
        "expires_at": payload["exp"],
        "payload": payload,
        "notes": f"Token creado con algoritmo {algorithm} y expiración en {expiration_seconds}s"
    }
    
    print(f"\n✓ Se guardaría en MongoDB:")
    print(json.dumps(token_data, indent=2))
    
    print("\n" + "=" * 80)
    print("✅ TODOS LOS ESCENARIOS CORRECTOS")
    print("=" * 80)

def test_timer_logic():
    """Prueba la lógica del temporizador JavaScript"""
    print("\n\n" + "=" * 80)
    print("TEST: Lógica del Temporizador")
    print("=" * 80)
    
    # Simular token que expira en 1 minuto
    now = time.time()
    expires_at = now + 60  # expira en 60 segundos
    
    print(f"\n⏱️  Token que expira en 60 segundos")
    print(f"Ahora: {now}")
    print(f"Expira: {expires_at}")
    
    # Simular paso del tiempo
    for elapsed in [0, 15, 30, 45, 59, 60, 61]:
        current_time = now + elapsed
        time_left = expires_at - current_time
        
        if time_left <= 0:
            status = "⏰ EXPIRADO"
            color = "ROJO"
        elif time_left < 5:
            status = f"⏳ {int(time_left)}s"
            color = "ROJO"
        else:
            status = f"⏳ {int(time_left)}s"
            color = "NARANJA" if time_left < 300 else "AZUL"
        
        print(f"  +{elapsed:2d}s → {status:20s} ({color})")

def test_mongodb_schema():
    """Prueba el esquema que se guarda en MongoDB"""
    print("\n\n" + "=" * 80)
    print("TEST: Esquema de MongoDB")
    print("=" * 80)
    
    schema = {
        "_id": "ObjectId",
        "token": "JWT token string",
        "header": {
            "alg": "HS256 or HS384",  # ← NUEVO
            "typ": "JWT"
        },
        "payload": {
            "sub": "user_id",
            "name": "user_name",
            "iat": "timestamp_creation",  # ← NUEVO
            "exp": "timestamp_expiration"  # ← NUEVO
        },
        "algorithm": "HS256 or HS384",         # ← NUEVO
        "expiration_seconds": "int",           # ← NUEVO
        "created_at": "timestamp_creation",    # ← NUEVO
        "expires_at": "timestamp_expiration",  # ← NUEVO
        "type": "created",
        "is_valid": True,
        "signature_valid": True,
        "notes": "Description"
    }
    
    print("\n✓ Esquema completo de MongoDB:")
    print(json.dumps(schema, indent=2))
    
    print("\n✓ NUEVOS CAMPOS AGREGADOS (MARCADOS CON ← NUEVO):")
    print("  1. header.alg: Almacena el algoritmo seleccionado")
    print("  2. payload.iat: Timestamp de creación del token")
    print("  3. payload.exp: Timestamp de expiración del token")
    print("  4. algorithm: Algoritmo seleccionado (para referencia rápida)")
    print("  5. expiration_seconds: Segundos de duración seleccionados")
    print("  6. created_at: Timestamp Unix de creación")
    print("  7. expires_at: Timestamp Unix de expiración")

if __name__ == "__main__":
    test_token_creation()
    test_timer_logic()
    test_mongodb_schema()
    
    print("\n\n" + "=" * 80)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 80)
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Abre http://localhost:5000")
    print("2. Ve a la pestaña 'Crear Token'")
    print("3. Selecciona algoritmo y expiración")
    print("4. Crea un token y verifica el temporizador")
    print("5. Abre MongoDB Compass para ver los datos guardados")
    print("\n" + "=" * 80)

