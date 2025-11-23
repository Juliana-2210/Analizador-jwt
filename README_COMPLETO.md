# JWT Analyzer - Proyecto Final LF

Analizador especializado de JSON Web Tokens (JWT) que implementa todas las fases de análisis de lenguajes formales: análisis léxico, sintáctico y semántico, además de codificación, decodificación y validación criptográfica.

## 🎯 Objetivos del Proyecto

- ✅ Aplicar teoría de lenguajes formales para definir la gramática de JWT
- ✅ Implementar un analizador léxico para tokenización
- ✅ Construir un parser sintáctico
- ✅ Realizar análisis semántico y validación de estructura
- ✅ Implementar generación de código (encoding/decoding)
- ✅ Aplicar conceptos de criptografía en la verificación de firmas

## 📋 Estructura de JWT

Un JWT consta de tres partes separadas por puntos: `HEADER.PAYLOAD.SIGNATURE`

### Header (Encabezado)
- Campos obligatorios: `alg` (algoritmo), `typ` (tipo)
- Ejemplo: `{"alg":"HS256","typ":"JWT"}`

### Payload (Carga)
- Contiene claims (datos) del usuario
- Claims estándar: `iss`, `sub`, `exp`, `iat`, `nbf`, `aud`, `jti`
- Ejemplo: `{"sub":"1234567890","name":"John Doe","iat":1630000000,"exp":1630003600}`

### Signature (Firma)
- Firma criptográfica para validar integridad
- Algoritmos soportados: HS256, HS384

## 🚀 Instalación

### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📋 Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest -v

# Ejecutar tests específicos
pytest tests/test_jwt_valid.py -v
pytest tests/test_jwt_malformed.py -v
pytest tests/test_jwt_expired.py -v
pytest tests/test_jwt_bad_signature.py -v
pytest tests/test_jwt_incorrect_types.py -v
pytest tests/test_jwt_missing_fields.py -v
pytest tests/test_jwt_algorithms.py -v

# Mostrar cobertura
pytest --cov=jwt_analyzer tests/
```

## 🔧 Uso de la Interfaz Web

```bash
python app.py
```

Luego abre tu navegador en: `http://localhost:5000`

### Funcionalidades de la interfaz:
- **Decodificar JWT**: Mostrar header y payload en formato legible
- **Validar estructura**: Verificar sintaxis correcta (análisis léxico/sintáctico)
- **Validar semántica**: Verificar campos obligatorios y tipos de datos
- **Verificar firma**: Validar integridad criptográfica con secret
- **Codificar JWT**: Crear nuevo token desde JSON

## 💻 Uso CLI (Interfaz de Línea de Comandos)

### Decodificar un token
```bash
python -m jwt_analyzer.cli decode eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNjMwMDAwMDAwfQ.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```

### Crear un token
```bash
python -m jwt_analyzer.cli create --payload '{"sub":"1","iat":1630000000,"exp":1630003600}' --secret mysecret
```

### Validar un token
```bash
python -m jwt_analyzer.cli validate <token> --secret mysecret

# Sin verificar expiración
python -m jwt_analyzer.cli validate <token> --secret mysecret --skip-time
```

## 🎮 Demostración Interactiva

```bash
python demo.py
```

Muestra todos los casos de uso: creación, análisis, verificación, tokens expirados, etc.

## 🏗️ Arquitectura del Proyecto

### Fase 1: Análisis Léxico (`jwt_analyzer/lexer.py`)
- Tokenización de JWT en tres partes
- Validación de caracteres Base64URL
- Detección de estructura malformada

### Fase 2: Análisis Sintáctico (`jwt_analyzer/parser.py`)
- Decodificación Base64URL
- Parseo JSON de header y payload
- Gramática: `JWT → HEADER . PAYLOAD . SIGNATURE`

### Fase 3: Análisis Semántico (`jwt_analyzer/semantic.py`)
- Validación de campos obligatorios
- Validación de tipos de datos
- Validación de claims temporales (exp, iat, nbf)
- Tabla de símbolos para claims conocidos

### Fase 4: Decodificación
- Decodificador Base64URL (`jwt_analyzer/base64url.py`)
- Extracción de header y payload
- Visualización de claims

### Fase 5: Codificación (`jwt_analyzer/encoder.py`)
- Generador de header y payload
- Codificador Base64URL
- Serialización JSON

### Fase 6: Verificación Criptográfica (`jwt_analyzer/crypto_verify.py`)
- Verificación de firmas HMAC
- Soporte para HS256 y HS384
- Protección contra timing attacks

## 📊 Casos de Prueba Implementados

✅ **27 Tests Aprobados**

### ✅ Tokens Válidos
- Tokens válidos con diferentes algoritmos (HS256, HS384)
- Validación completa: sintaxis, semántica, firma

### ✅ Tokens Expirados
- Validación de claim `exp`
- Detección de tokens vencidos

### ✅ Tokens con Firma Inválida
- Falsificación de firma
- Verificación de integridad fallida

### ✅ Tokens Malformados
- Estructura incorrecta (menos de 3 partes)
- Caracteres inválidos en Base64URL
- JSON inválido en header/payload

### ✅ Tokens con Tipos Incorrectos
- `exp`, `iat`, `nbf` como string en lugar de número
- Header/payload como array en lugar de objeto

### ✅ Tokens con Campos Faltantes
- Header sin campo `alg` o `typ`
- Claims sin los campos requeridos
- Algoritmo no soportado

## 📁 Estructura de Carpetas

```
lenguajes/
├── jwt_analyzer/              # Módulo principal
│   ├── __init__.py
│   ├── lexer.py              # Análisis léxico
│   ├── parser.py             # Análisis sintáctico
│   ├── semantic.py           # Análisis semántico
│   ├── encoder.py            # Codificación
│   ├── crypto_verify.py      # Verificación criptográfica
│   ├── base64url.py          # Base64URL encoding/decoding
│   ├── cli.py                # Interfaz de línea de comandos
│   └── utils.py              # Utilidades
├── tests/                     # Suite de pruebas (27 tests)
│   ├── conftest.py
│   ├── test_jwt_valid.py
│   ├── test_jwt_malformed.py
│   ├── test_jwt_expired.py
│   ├── test_jwt_bad_signature.py
│   ├── test_jwt_incorrect_types.py
│   ├── test_jwt_missing_fields.py
│   └── test_jwt_algorithms.py
├── templates/                 # Plantillas Flask
│   ├── index_improved.html   # Interfaz web mejorada
│   └── index.html
├── static/                    # Archivos estáticos
│   └── styles.css             # Estilos profesionales
├── app.py                     # Aplicación Flask
├── demo.py                    # Demostración interactiva
└── requirements.txt           # Dependencias
```

## 🔍 Ejemplos de Uso

### Ejemplo 1: Crear y validar un token

```python
from jwt_analyzer.encoder import encode_jwt
from jwt_analyzer.parser import JWTParser
from jwt_analyzer.semantic import validate_header, validate_payload
from jwt_analyzer.crypto_verify import verify_signature
import time

# Crear header y payload
header = {"alg": "HS256", "typ": "JWT"}
payload = {
    "sub": "1234567890",
    "name": "John Doe",
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600
}

# Codificar
secret = b"mysecret"
token = encode_jwt(header, payload, secret)
print(f"Token: {token}")

# Parsear
parser = JWTParser()
parsed = parser.parse(token)

# Validar semántica
validate_header(parsed["header"])
validate_payload(parsed["payload"])

# Verificar firma
is_valid = verify_signature(
    parsed["header_b64"],
    parsed["payload_b64"],
    parsed["signature"],
    secret,
    "HS256"
)
print(f"Firma válida: {is_valid}")
```

### Ejemplo 2: Decodificar un token

```python
from jwt_analyzer.parser import JWTParser
import json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0..."

parser = JWTParser()
parsed = parser.parse(token)

print("Header:")
print(json.dumps(parsed["header"], indent=2))

print("\nPayload:")
print(json.dumps(parsed["payload"], indent=2))
```

## 🛡️ Seguridad

- Verificación de firma con `hmac.compare_digest()` para evitar timing attacks
- Validación de tipos para prevenir inyecciones de JSON
- Validación de claims temporales
- Soporte solo para algoritmos HMAC (HS256, HS384)

## 📚 Referencias

- [JWT.io - Introduction](https://jwt.io/introduction)
- [RFC 7519 - JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519)
- [HMAC - Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)

## ✨ Estado del Proyecto

| Fase | Componente | Estado |
|------|-----------|--------|
| 1 | Análisis Léxico | ✅ Completado |
| 2 | Análisis Sintáctico | ✅ Completado |
| 3 | Análisis Semántico | ✅ Completado |
| 4 | Decodificación | ✅ Completado |
| 5 | Codificación | ✅ Completado |
| 6 | Verificación Criptográfica | ✅ Completado |
| | Tests Unitarios | ✅ 27/27 pasados |
| | Interfaz Web | ✅ Mejorada |
| | CLI | ✅ Funcional |
| | Demostración | ✅ Completa |

## 👤 Autor

Desarrollado como Proyecto Final del curso de Lenguajes Formales

---

**Última actualización**: Noviembre 2025
