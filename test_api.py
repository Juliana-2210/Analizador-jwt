#!/usr/bin/env python3
"""
Script para probar las APIs REST de MongoDB
Necesita que la app esté corriendo: python app.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("JWT ANALYZER - PRUEBA DE APIS REST")
print("=" * 80)
print("\n⚠️  ASEGÚRATE QUE LA APP ESTÉ CORRIENDO: python app.py\n")

time.sleep(2)

try:
    # Test 1: Ver todos los tokens
    print("1️⃣  Obteniendo todos los tokens...\n")
    response = requests.get(f"{BASE_URL}/api/tokens")
    if response.status_code == 200:
        tokens = response.json()
        print(f"✅ {len(tokens)} tokens encontrados\n")
        if tokens:
            print("Primeros 3 tokens:")
            for token in tokens[:3]:
                print(f"   - {token.get('_id', 'unknown')}: {token.get('type')}")
    else:
        print(f"❌ Error: {response.status_code}\n")
    
    # Test 2: Ver estadísticas
    print("\n2️⃣  Obteniendo estadísticas...\n")
    response = requests.get(f"{BASE_URL}/api/statistics")
    if response.status_code == 200:
        stats = response.json()
        print("✅ Estadísticas:")
        print(f"   Total: {stats.get('total', 0)}")
        print(f"   Válidos: {stats.get('valid', 0)}")
        print(f"   Inválidos: {stats.get('invalid', 0)}")
        print(f"   Expirados: {stats.get('expired', 0)}")
    else:
        print(f"❌ Error: {response.status_code}\n")
    
    # Test 3: Crear una colección
    print("\n3️⃣  Creando una colección de prueba...\n")
    collection_data = {
        "name": "Prueba API",
        "description": "Colección de prueba para validar API"
    }
    response = requests.post(
        f"{BASE_URL}/api/collections",
        json=collection_data,
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 201:
        result = response.json()
        collection_id = result.get("collection_id")
        print(f"✅ Colección creada: {collection_id}\n")
        
        # Test 4: Ver la colección
        print("4️⃣  Obteniendo la colección creada...\n")
        response = requests.get(f"{BASE_URL}/api/collections/{collection_id}")
        if response.status_code == 200:
            collection = response.json()
            print(f"✅ Colección: {collection.get('name')}")
            print(f"   Descripción: {collection.get('description')}")
            print(f"   Tokens: {len(collection.get('tokens', []))}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text}\n")
    
    # Test 5: Ver todas las colecciones
    print("\n5️⃣  Obteniendo todas las colecciones...\n")
    response = requests.get(f"{BASE_URL}/api/collections")
    if response.status_code == 200:
        collections = response.json()
        print(f"✅ {len(collections)} colecciones encontradas\n")
        for coll in collections[:5]:
            print(f"   - {coll.get('name')}: {len(coll.get('tokens', []))} tokens")
    else:
        print(f"❌ Error: {response.status_code}\n")
    
    print("\n" + "=" * 80)
    print("✅ PRUEBA DE APIS COMPLETADA")
    print("=" * 80)
    print("\n📚 ENDPOINTS DISPONIBLES:\n")
    print("Tokens:")
    print("  GET    /api/tokens")
    print("  POST   /api/tokens")
    print("  GET    /api/tokens/<id>")
    print("  DELETE /api/tokens/<id>")
    print("  GET    /api/statistics")
    print("\nColecciones:")
    print("  GET    /api/collections")
    print("  POST   /api/collections")
    print("  GET    /api/collections/<id>")
    print("  DELETE /api/collections/<id>")
    print("  POST   /api/collections/<id>/tokens/<token_id>")
    print("  DELETE /api/collections/<id>/tokens/<token_id>")
    
except requests.exceptions.ConnectionError:
    print("❌ ERROR DE CONEXIÓN")
    print("\n⚠️  La aplicación no está corriendo")
    print("\nEjecuta en otra terminal:")
    print("   python app.py")
    print("\nLuego ejecuta este script nuevamente")

except Exception as e:
    print(f"❌ Error inesperado: {e}")
