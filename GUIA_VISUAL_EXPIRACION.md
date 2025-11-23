# 🎨 GUÍA VISUAL: Sistema de Expiración en Acción

## 🌐 Vista de la Aplicación

```
════════════════════════════════════════════════════════════════════════════════
                          JWT ANALYZER - Análisis Completo
                     Decodifica, valida y crea tokens JWT
════════════════════════════════════════════════════════════════════════════════

[📊 Analizar Token]  [➕ Crear Token]  [🧪 Casos de Prueba]
                     ▲ Haz clic aquí
```

---

## 🎯 PESTAÑA: CREAR TOKEN

### VISTA 1: Formulario Completo

```
╔════════════════════════════════════════════════════════════════════════════╗
║                     ➕ Crear Nuevo Token JWT                              ║
╚════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────┐
│ 🔑 Algoritmo de Firma               ⏱️  Expiración del Token             │
│ ┌────────────────────────────────┐  ┌─────────────────────────────────┐ │
│ │ ▼ HS256 (SHA-256)   [SELECTOR] │  │ ▼ 1 hora         [SELECTOR]     │ │
│ │   HS384 (SHA-384)               │  │   5 minutos                      │ │
│ │   [CLIC PARA MÁS OPCIONES]     │  │   10 minutos                     │ │
│ └────────────────────────────────┘  │   30 minutos                     │ │
│ Selecciona el algoritmo HMAC para   │   24 horas                       │ │
│ firmar el token.                    │   7 días                         │ │
│                                     │   30 días                        │ │
│                                     └─────────────────────────────────┘ │
│                                     El token expirará después de         │
│                                     este tiempo.                         │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ Payload JSON                                                             │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ {                                                                   │ │
│ │   "sub": "user123",                                                │ │
│ │   "name": "John Doe",                                              │ │
│ │   "email": "john@example.com"                                      │ │
│ │ }                                                                   │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ Ingresa el payload como JSON válido (sin iat ni exp, se agregan        │
│ automáticamente).                                                       │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ Secret para Firmar                                                       │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ ••••••••••••••••••      [CAMPO DE CONTRASEÑA]                      │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│ Se usará para firmar el token con el algoritmo seleccionado.           │
└──────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────┐
    │  ⚡ Crear Token JWT                                         │
    │  [100% WIDTH BUTTON - VERDE]                              │
    └─────────────────────────────────────────────────────────────┘
```

---

## ✅ RESULTADO: Token Creado Exitosamente

### VISTA 2: Temporizador en Vivo (NUEVA FUNCIONALIDAD)

```
╔════════════════════════════════════════════════════════════════════════════╗
║                   ✓ Token Creado Exitosamente                             ║
╚════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────┐
│ ⏳ TEMPORIZADOR DE EXPIRACIÓN                        [CUADRO NARANJA]    │
│ ┌────────────────────────────────────┬──────────────────────────────┐   │
│ │ Tiempo Restante:                    │ Algoritmo: HS256             │   │
│ │ ⏳ 59m 45s                          │ Guardado en BD: ✓ SÍ         │   │
│ │                                     │ (Token ID: 6922517b...)      │   │
│ │ [COLOR AZUL: tiempo normal]        │                              │   │
│ │ [COLOR NARANJA: < 5 minutos]       │                              │   │
│ │ [COLOR ROJO: < 1 minuto]           │                              │   │
│ │ [ROJO CON "EXPIRADO" al llegar a 0]│                              │   │
│ └────────────────────────────────────┴──────────────────────────────┘   │
│                                                                          │
│ ✓ Se actualiza AUTOMÁTICAMENTE cada segundo                             │
│ ✓ Puedes refrescar la página y verá el tiempo actualizado               │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ Tu nuevo JWT:                                                            │
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNzAwNjgwOTAwLCJleHAiOjE3MDA2ODI3MDB9.SIGNATURE... │
│ │                                                                     │ │
│ │ [PALABRA BREAK - Se ajusta al ancho]                               │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ Partes del Token:                                                        │
│                                                                          │
│ [HEADER - Azul]   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9               │
│ [PAYLOAD - Verde] eyJzdWIiOiJ1c2VyMTIzIiwibmFtZSI6IkpvaG4gRG9l...  │
│ [FIRMA - Rojo]    SIGNATURE123456789...                               │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ ℹ️  INFORMACIÓN:                                                          │
│                                                                          │
│ 1. Regresa a la pestaña "Analizar Token"                               │
│ 2. Pega el token en el campo de entrada                                │
│ 3. Proporciona el mismo secret que usaste para crear                  │
│ 4. Haz clic en "Analizar Token Completo"                              │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## ⏱️ TEMPORIZADOR EN ACCIÓN (Simulación)

```
Tiempo Inicial:    ⏳ 1h 0m 0s    [AZUL]
                   ↓

Después 30 min:    ⏳ 0h 30m 0s   [AZUL]
                   ↓

A los 55 min:      ⏳ 0h 5m 0s    [NARANJA] ← Cambia de color
                   ↓

A los 59 min:      ⏳ 0h 1m 0s    [ROJO] ← Alerta final
                   ↓

Cuando expira:     ⏰ EXPIRADO     [ROJO OSCURO]
```

---

## 💾 LO QUE SE GUARDA EN MONGODB

Cuando creas el token, la base de datos recibe:

```json
{
  "_id": ObjectId("674123abcd4567890abc1234"),
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWI...",
  "header": {
    "alg": "HS256",      ← EL ALGORITMO QUE SELECCIONASTE
    "typ": "JWT"
  },
  "payload": {
    "sub": "user123",
    "name": "John Doe",
    "email": "john@example.com",
    "iat": 1700680900,   ← CREADO A ESTA HORA
    "exp": 1700684500    ← EXPIRA A ESTA HORA (iat + 3600)
  },
  "signature": "...",
  "type": "created",
  "is_valid": true,
  "signature_valid": true,
  "algorithm": "HS256",           ← GUARDADO PARA REFERENCIA
  "expiration_seconds": 3600,     ← LOS SEGUNDOS QUE SELECCIONASTE
  "created_at": 1700680900,       ← TIMESTAMP DE CREACIÓN
  "expires_at": 1700684500,       ← TIMESTAMP DE EXPIRACIÓN
  "notes": "Token creado con algoritmo HS256 y expiración en 3600s",
  "createdAt": ISODate("2025-11-22T19:35:00.000Z")
}
```

---

## 🎬 DEMO PASO A PASO EN VIVO

### Escenario 1: Token que expira en 5 minutos

```
PASO 1: Selecciona algoritmo
        ▼ HS384 (SHA-384)

PASO 2: Selecciona expiración
        ▼ 5 minutos

PASO 3: Ingresa payload
        {
          "user_id": "admin001",
          "permissions": ["read", "write"]
        }

PASO 4: Ingresa secret
        MyAdminSecret2024!

PASO 5: Clic en "Crear Token JWT"

RESULTADO:
═════════════════════════════════════════
✅ Token Creado Exitosamente

⏳ 4m 59s    [COLOR NARANJA - ALERTA INMEDIATA]
             (Menos de 5 minutos)

Algoritmo: HS384
Guardado en BD: ✓ SÍ (ID: abc123def456)

Token JWT:
eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWRtaW4wMDEiLCJwZXJtaXNzaW9ucyI6WyJyZWFkIiwid3JpdGUiXSwiaWF0IjoxNzAwNjgwOTAwLCJleHAiOjE3MDA2ODExMDB9.SIGNATURE...

═════════════════════════════════════════

EL TEMPORIZADOR SE ACTUALIZA CADA SEGUNDO:
4m 58s
4m 57s
4m 56s
...
1m 30s [SIGUE NARANJA]
...
0m 59s [CAMBIA A ROJO]
0m 58s
...
0m 1s  [ROJO OSCURO]
⏰ EXPIRADO [DETENIDO]
```

---

## 📊 COMPARACIÓN: ANTES vs DESPUÉS

### ANTES (Sin esta característica)

```
"Crear Token"
├─ Solo HS256
├─ Sin selector de expiración
├─ Sin datos de expiración en respuesta
└─ Sin temporizador visual
```

### DESPUÉS (Con esta característica)

```
"Crear Token" ✨ MEJORADO
├─ ✅ Selector HS256/HS384
├─ ✅ Selector 5min-30días
├─ ✅ Temporizador en vivo
├─ ✅ Guarda algorithm en BD
├─ ✅ Guarda exp en BD
├─ ✅ Guarda expiration_seconds en BD
└─ ✅ Guarda created_at en BD
```

---

## 🔍 VISUALIZACIÓN EN MONGODB

Si abres MongoDB Compass:

```
Database: jwt_analyzer
Collection: tokens

Document:
{
  _id: ObjectId("674123...")
  ├─ token: "eyJ..."
  ├─ header: {alg: "HS256"}
  ├─ payload: {
  │   ├─ sub: "user123"
  │   ├─ iat: 1700680900      ← CREATED
  │   └─ exp: 1700684500      ← EXPIRES
  │
  ├─ algorithm: "HS256"       ← DEL SELECTOR
  ├─ expiration_seconds: 3600 ← DEL SELECTOR
  ├─ created_at: 1700680900
  ├─ expires_at: 1700684500
  └─ notes: "Token creado con algoritmo HS256 y expiración en 3600s"
}
```

---

## 💻 CÓDIGO BACKEND (app.py)

Lo que sucede cuando presionas "Crear Token JWT":

```python
# ENTRADA DEL USUARIO
algorithm = request.form.get("algorithm", "HS256")      # ← HS256 o HS384
expiration_time = request.form.get("expiration_time")   # ← 300, 3600, etc.
payload_json = request.form.get("payload_new")          # ← {"sub": "user"}
secret = request.form.get("secret_new")                 # ← "MySecret"

# PROCESAMIENTO
payload_obj = json.loads(payload_json)
now = int(time.time())
payload_obj["iat"] = now
payload_obj["exp"] = now + int(expiration_time)

# CREACIÓN DEL TOKEN
header = {"alg": algorithm, "typ": "JWT"}
token = encode_jwt(header, payload_obj, secret.encode())

# GUARDADO EN MONGODB
if mongo.is_connected():
    token_data = {
        "token": token,
        "header": header,
        "payload": payload_obj,
        "algorithm": algorithm,           # ← ALGORITMO
        "expiration_seconds": expiration_time,  # ← DURACIÓN
        "created_at": now,               # ← TIMESTAMP CREACIÓN
        "expires_at": payload_obj["exp"],# ← TIMESTAMP EXPIRACION
        "notes": f"Token creado con algoritmo {algorithm}..."
    }
    token_id = TokenRepository.save_token(token_data)

# RETORNO AL FRONTEND
return {
    "algorithm": algorithm,
    "expires_at": payload_obj["exp"],
    "expiration_seconds": expiration_time
}
```

---

## 🎯 PARA MOSTRAR A LOS PROFESORES

**Demostración en 3 minutos:**

1. **Abre la pestaña "Crear Token"** (30 segundos)
2. **Selecciona HS384 y 5 minutos** (15 segundos)
3. **Ingresa datos y crea token** (30 segundos)
4. **Muestra el temporizador contando** (60 segundos)
5. **Abre MongoDB para mostrar el guardado** (30 segundos)
6. **Explica la relación iat/exp** (30 segundos)

---

## ✅ CHECKLIST DE VERIFICACIÓN

- [ ] La pestaña "Crear Token" muestra los 2 selectores
- [ ] El selector de algoritmo funciona (HS256/HS384)
- [ ] El selector de expiración muestra 7 opciones
- [ ] Al crear token aparece el temporizador
- [ ] El temporizador actualiza cada segundo
- [ ] El color cambia: azul → naranja → rojo
- [ ] El token se guarda en MongoDB
- [ ] MongoDB tiene los campos: algorithm, expiration_seconds, created_at, expires_at
- [ ] El temporizador se actualiza correctamente (iat/exp en payload)
- [ ] Cuando expira muestra "⏰ EXPIRADO"

---

**¡Sistema completamente visualizado y funcional!** 🎉

