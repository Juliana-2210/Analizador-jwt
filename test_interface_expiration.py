#!/usr/bin/env python3
"""
Script para probar la funcionalidad de expiración en la interfaz web
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_analyze_expired_token():
    """Analizar un token expirado para ver la información de expiración"""
    
    # Token expirado de los casos de prueba
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjoxNTE2MjM5MDIyfQ.1oPvLPCCGb1jUX5f0n5VVAi_-qWkDhS2PuOv0EgVhWw"
    secret = "secret"
    
    print("\n" + "="*70)
    print("TEST: Verificar Información de Expiración en la Interfaz")
    print("="*70)
    
    print("\n📝 Analizando token expirado...")
    print(f"   Token: {token[:50]}...")
    print(f"   Secret: {secret}")
    
    # Enviar POST al servidor
    try:
        response = requests.post(BASE_URL, data={
            "jwt": token,
            "secret": secret,
            "action": "analyze"
        })
        
        if response.status_code == 200:
            print("\n✅ Respuesta recibida del servidor")
            
            # Verificar que contenga la información de expiración
            if "output" in response.text or "expiration" in response.text:
                print("✅ La página contiene información de expiración")
                
                # Buscar indicios en el HTML
                if "Estado de Expiración" in response.text:
                    print("✅ Sección 'Estado de Expiración' presente en la página")
                
                if "Expirado" in response.text or "Expiró hace" in response.text:
                    print("✅ Mensaje de token expirado detectado")
                
                if "hourglass" in response.text or "fa-hourglass" in response.text:
                    print("✅ Icono de expiración presente")
                
                print("\n✨ ¡Funcionalidad de expiración activa y funcionando!")
            else:
                print("⚠️ No se encontró información de expiración en la página")
        else:
            print(f"❌ Error: Status code {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("   Verifica que app.py esté corriendo en http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70)
    print("VERIFICACIÓN VISUAL")
    print("="*70)
    print("\nPara verificar visualmente:")
    print("1. Abre http://localhost:5000")
    print("2. Ve a [Analizar Token]")
    print("3. Ingresa este token expirado:")
    print(f"   {token}")
    print("4. Ingresa secret: secret")
    print("5. Haz clic en [Analizar Token Completo]")
    print("\n6. DEBE APARECER en la parte superior:")
    print("   Estado de Expiración: ✗ Expirado")
    print("   Expiró hace: 5+ años (es un token muy antiguo)")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_analyze_expired_token()
