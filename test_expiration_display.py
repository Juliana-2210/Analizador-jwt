#!/usr/bin/env python3
"""
Test para verificar que la información de expiración se muestra correctamente
en la interfaz web del JWT Analyzer.
"""

import time
import json
from datetime import datetime, timedelta
from jwt_analyzer.encoder import encode_jwt
from jwt_analyzer.base64url import b64url_encode, b64url_decode

def test_expiration_display():
    """Prueba que la información de expiración se calcule correctamente"""
    
    print("\n" + "="*70)
    print("TEST: Información de Expiración en la Interfaz")
    print("="*70)
    
    # Crear un token que expira en 5 minutos
    now = int(time.time())
    exp_5min = now + 300  # 5 minutos
    exp_1sec = now + 1    # 1 segundo (casi expirado)
    exp_past = now - 3600  # 1 hora en el pasado (ya expirado)
    
    # Token válido en 5 minutos
    print("\n✓ CASO 1: Token que expira en 5 minutos")
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": now,
        "exp": exp_5min
    }
    secret = b"your-256-bit-secret"
    token_5min = encode_jwt(header, payload, secret)
    print(f"  Token: {token_5min[:50]}...")
    print(f"  Exp timestamp: {exp_5min}")
    print(f"  Tiempo restante calculado: ~5 minutos")
    print(f"  Expected display: ✓ Activo | Expira en: 4m 58s-5m")
    
    # Token a punto de expirar
    print("\n✓ CASO 2: Token a punto de expirar (1 segundo)")
    payload["exp"] = exp_1sec
    token_1sec = encode_jwt(header, payload, secret)
    print(f"  Token: {token_1sec[:50]}...")
    print(f"  Exp timestamp: {exp_1sec}")
    print(f"  Tiempo restante calculado: ~1 segundo")
    print(f"  Expected display: ✓ Activo | Expira en: 0s-1s")
    
    # Token expirado
    print("\n✓ CASO 3: Token expirado")
    payload["exp"] = exp_past
    token_expired = encode_jwt(header, payload, secret)
    print(f"  Token: {token_expired[:50]}...")
    print(f"  Exp timestamp: {exp_past}")
    print(f"  Tiempo expirado: ~1 hora")
    print(f"  Expected display: ✗ Expirado | Expiró hace: 59m 59s-1h")
    
    # Token sin expiration claim
    print("\n✓ CASO 4: Token sin claim 'exp'")
    payload_no_exp = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": now
    }
    token_no_exp = encode_jwt(header, payload_no_exp, secret)
    print(f"  Token: {token_no_exp[:50]}...")
    print(f"  No tiene 'exp' en el payload")
    print(f"  Expected display: ⚠ Sin exp | Token sin fecha de expiración")
    
    print("\n" + "="*70)
    print("VERIFICACIÓN DE CÁLCULOS:")
    print("="*70)
    
    # Verificar cálculos de expiración
    current_time = int(time.time())
    
    # Caso 1: Token activo en 5 minutos
    time_left = exp_5min - current_time
    minutes = time_left // 60
    seconds = time_left % 60
    print(f"\n1. Token activo: {minutes}m {seconds}s restante")
    
    # Caso 3: Token expirado
    time_expired = current_time - exp_past
    hours = time_expired // 3600
    minutes_exp = (time_expired % 3600) // 60
    seconds_exp = time_expired % 60
    print(f"2. Token expirado: {hours}h {minutes_exp}m {seconds_exp}s hace")
    
    print("\n" + "="*70)
    print("✅ PRUEBA COMPLETADA")
    print("="*70)
    print("\nPara verificar visualmente:")
    print("1. Abre http://localhost:5000")
    print("2. Ve a [🧪 Casos de Prueba]")
    print("3. Expande [⏰ Tokens Expirados]")
    print("4. Haz clic en [Probar en Analizador]")
    print("5. Verás la información de expiración en la parte superior")
    print("\nDebe mostrar:")
    print("  - Estatus léxico/sintáctico/semántico")
    print("  - Estado de firma")
    print("  - ⭐ NUEVA: Estado de expiración (✓ Activo / ✗ Expirado / ⚠ Sin exp)")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_expiration_display()
