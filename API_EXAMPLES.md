# 🔌 EJEMPLOS DE USO DE APIs REST

## 📝 Introducción

Una vez que configures MongoDB Atlas y ejecutes `python app.py`, puedes usar estas APIs para interactuar con los tokens y colecciones.

---

## 1️⃣ TOKENS - Obtener todos

### Con cURL
```bash
curl http://localhost:5000/api/tokens
```

### Con Python
```python
import requests

response = requests.get("http://localhost:5000/api/tokens")
tokens = response.json()

for token in tokens:
    print(f"ID: {token['_id']}")
    print(f"Tipo: {token['type']}")
    print(f"Válido: {token['is_valid']}")
    print()
```

### Con JavaScript/Fetch
```javascript
fetch('http://localhost:5000/api/tokens')
  .then(r => r.json())
  .then(tokens => {
    tokens.forEach(token => {
      console.log(`${token._id}: ${token.type}`);
    });
  });
```

---

## 2️⃣ TOKENS - Obtener uno específico

```bash
curl http://localhost:5000/api/tokens/507f1f77bcf86cd799439011
```

**Respuesta:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "header": {"alg": "HS256", "typ": "JWT"},
  "payload": {"sub": "1234567890"},
  "type": "valid",
  "is_valid": true,
  "created_at": "2025-11-22T10:30:00Z"
}
```

---

## 3️⃣ TOKENS - Guardar un nuevo token

### Con cURL
```bash
curl -X POST http://localhost:5000/api/tokens \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJ...",
    "header": {"alg": "HS256", "typ": "JWT"},
    "payload": {"sub": "123"},
    "type": "valid",
    "is_valid": true,
    "algorithm": "HS256"
  }'
```

### Con Python
```python
import requests

token_data = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "header": {"alg": "HS256", "typ": "JWT"},
    "payload": {"sub": "1234567890", "name": "John"},
    "type": "valid",
    "is_valid": True,
    "signature_valid": True,
    "algorithm": "HS256",
    "notes": "Token de prueba"
}

response = requests.post(
    "http://localhost:5000/api/tokens",
    json=token_data
)

result = response.json()
print(f"Token guardado con ID: {result['token_id']}")
```

---

## 4️⃣ TOKENS - Eliminar un token

```bash
curl -X DELETE http://localhost:5000/api/tokens/507f1f77bcf86cd799439011
```

**Respuesta:**
```json
{"success": true}
```

---

## 5️⃣ TOKENS - Obtener estadísticas

```bash
curl http://localhost:5000/api/statistics
```

**Respuesta:**
```json
{
  "total": 45,
  "valid": 38,
  "invalid": 5,
  "expired": 2
}
```

---

## 6️⃣ COLECCIONES - Obtener todas

```bash
curl http://localhost:5000/api/collections
```

**Respuesta:**
```json
[
  {
    "_id": "507f191e810c19729de860ea",
    "name": "Tokens de Desarrollo",
    "description": "Colección de tokens para desarrollo",
    "tokens": ["id1", "id2", "id3"],
    "created_at": "2025-11-22T10:00:00Z"
  }
]
```

---

## 7️⃣ COLECCIONES - Crear una nueva

### Con cURL
```bash
curl -X POST http://localhost:5000/api/collections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tokens de Producción",
    "description": "Tokens para usar en producción"
  }'
```

### Con Python
```python
import requests

collection_data = {
    "name": "Tokens de API",
    "description": "Tokens para acceso a APIs externas"
}

response = requests.post(
    "http://localhost:5000/api/collections",
    json=collection_data
)

result = response.json()
collection_id = result['collection_id']
print(f"Colección creada: {collection_id}")
```

---

## 8️⃣ COLECCIONES - Ver una específica

```bash
curl http://localhost:5000/api/collections/507f191e810c19729de860ea
```

---

## 9️⃣ COLECCIONES - Agregar token a colección

```bash
curl -X POST \
  http://localhost:5000/api/collections/507f191e810c19729de860ea/tokens/507f1f77bcf86cd799439011 \
  -H "Content-Type: application/json"
```

### Con Python
```python
import requests

collection_id = "507f191e810c19729de860ea"
token_id = "507f1f77bcf86cd799439011"

response = requests.post(
    f"http://localhost:5000/api/collections/{collection_id}/tokens/{token_id}"
)

print("Token agregado a colección")
```

---

## 🔟 COLECCIONES - Quitar token de colección

```bash
curl -X DELETE \
  http://localhost:5000/api/collections/507f191e810c19729de860ea/tokens/507f1f77bcf86cd799439011
```

---

## 1️⃣1️⃣ COLECCIONES - Eliminar una colección

```bash
curl -X DELETE http://localhost:5000/api/collections/507f191e810c19729de860ea
```

---

## 📋 SCRIPT COMPLETO DE EJEMPLO

```python
#!/usr/bin/env python3
"""
Ejemplo completo de uso de las APIs del JWT Analyzer
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

# 1. Crear una colección
print_section("1. Crear una colección")

collection_data = {
    "name": "Colección de Ejemplo",
    "description": "Mi primera colección de tokens"
}

response = requests.post(
    f"{BASE_URL}/api/collections",
    json=collection_data
)
collection_result = response.json()
collection_id = collection_result['collection_id']
print(f"✅ Colección creada: {collection_id}")

# 2. Guardar tokens
print_section("2. Guardar tokens")

tokens = [
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwibmFtZSI6IkpvaG4ifQ...",
        "header": {"alg": "HS256", "typ": "JWT"},
        "payload": {"sub": "1", "name": "John"},
        "type": "valid",
        "is_valid": True,
        "algorithm": "HS256"
    },
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwibmFtZSI6IkphbmUifQ...",
        "header": {"alg": "HS256", "typ": "JWT"},
        "payload": {"sub": "2", "name": "Jane"},
        "type": "valid",
        "is_valid": True,
        "algorithm": "HS256"
    }
]

token_ids = []
for token_data in tokens:
    response = requests.post(f"{BASE_URL}/api/tokens", json=token_data)
    result = response.json()
    token_ids.append(result['token_id'])
    print(f"✅ Token guardado: {result['token_id']}")

# 3. Agregar tokens a la colección
print_section("3. Agregar tokens a la colección")

for token_id in token_ids:
    response = requests.post(
        f"{BASE_URL}/api/collections/{collection_id}/tokens/{token_id}"
    )
    print(f"✅ Token {token_id} agregado a colección")

# 4. Ver la colección
print_section("4. Ver la colección con todos sus tokens")

response = requests.get(f"{BASE_URL}/api/collections/{collection_id}")
collection = response.json()
print(json.dumps(collection, indent=2))

# 5. Ver estadísticas
print_section("5. Ver estadísticas")

response = requests.get(f"{BASE_URL}/api/statistics")
stats = response.json()
print(f"Total de tokens: {stats['total']}")
print(f"Válidos: {stats['valid']}")
print(f"Inválidos: {stats['invalid']}")
print(f"Expirados: {stats['expired']}")

# 6. Ver todos los tokens
print_section("6. Ver todos los tokens guardados")

response = requests.get(f"{BASE_URL}/api/tokens")
tokens = response.json()
print(f"Se encontraron {len(tokens)} tokens\n")

for token in tokens[:3]:  # Mostrar solo los primeros 3
    print(f"ID: {token['_id']}")
    print(f"Tipo: {token['type']}")
    print(f"Válido: {token['is_valid']}")
    print()

print_section("✅ Ejemplo completado")
```

---

## 🧪 PROBAR CON POSTMAN

1. Descarga [Postman](https://www.postman.com/downloads/)
2. Crea una nueva colección
3. Agrega requests para cada endpoint
4. Usa los ejemplos de arriba

**Ejemplo request en Postman:**
```
Method: POST
URL: http://localhost:5000/api/tokens
Headers: Content-Type: application/json
Body (raw):
{
  "token": "eyJ...",
  "header": {"alg": "HS256", "typ": "JWT"},
  "payload": {"sub": "123"},
  "type": "valid",
  "is_valid": true,
  "algorithm": "HS256"
}
```

---

## 🔄 FLUJO TÍPICO

1. **Crear token en la web** → Se guarda automáticamente en MongoDB
2. **Obtener token via API** → `/api/tokens`
3. **Crear colección** → `/api/collections` (POST)
4. **Agregar token a colección** → `/api/collections/<id>/tokens/<token_id>` (POST)
5. **Ver colección completa** → `/api/collections/<id>` (GET)
6. **Ver estadísticas** → `/api/statistics` (GET)

---

**¡Listo para usar!** 🚀
