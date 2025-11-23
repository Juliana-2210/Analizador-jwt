# ✨ NUEVO: Sistema Avanzado de Expiración de Tokens

## 📋 Resumen

Se ha implementado un **sistema completo de manejo de expiración de tokens JWT** con:

1. ✅ **Selector de Algoritmo** (HS256 o HS384)
2. ✅ **Selector de Duración** (5 min a 30 días)
3. ✅ **Temporizador en Vivo** (cuenta regresiva)
4. ✅ **Persistencia en MongoDB** (guarda exp en base de datos)

---

## 🎯 CÓMO FUNCIONA

### Paso 1: Abre la Pestaña "Crear Token"

```
http://localhost:5000
↓
Haz clic en pestaña [Crear Token]
```

### Paso 2: Selecciona los Parámetros

**Algoritmo:**
```
┌─ Algoritmo de Firma ────────────┐
│ ▼ HS256 (SHA-256) ← SELECCIONA │
│   HS384 (SHA-384)               │
└─────────────────────────────────┘
```

**Expiración:**
```
┌─ Expiración del Token ──────────────┐
│ ▼ 1 hora ← OPCIÓN POR DEFECTO       │
│   5 minutos                         │
│   10 minutos                        │
│   30 minutos                        │
│   24 horas                          │
│   7 días                            │
│   30 días                           │
└─────────────────────────────────────┘
```

### Paso 3: Ingresa el Payload

```json
{
  "sub": "user123",
  "name": "Juan Pérez",
  "email": "juan@example.com"
}
```

**NOTA:** No necesitas agregar `iat` ni `exp`, se agregan **automáticamente**

### Paso 4: Ingresa el Secret

```
Super-Secret-Key-2024
```

### Paso 5: Haz Clic en "Crear Token JWT"

---

## ⏰ TEMPORIZADOR EN VIVO

Una vez creado el token, aparece un **temporizador en tiempo real**:

```
┌──────────────────────────────────────────┐
│ ⏳ 1h 0m 0s                               │
│ (Azul: Normal)                           │
│ (Naranja: Últimos 5 minutos)            │
│ (Rojo: Último minuto)                    │
│                                          │
│ Algoritmo: HS256                         │
│ Guardado en BD: ✓ SÍ                     │
└──────────────────────────────────────────┘
```

**El temporizador se actualiza cada segundo** sin que tengas que refrescar.

---

## 💾 QUÉ SE GUARDA EN MONGODB

Cuando creas un token, se guarda:

```javascript
{
  "_id": ObjectId("..."),
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "header": {
    "alg": "HS256",      // ← ALGORITMO SELECCIONADO
    "typ": "JWT"
  },
  "payload": {
    "sub": "user123",
    "name": "Juan Pérez",
    "iat": 1700680000,   // ← ISSUED AT (automático)
    "exp": 1700683600    // ← EXPIRATION (automático)
  },
  "algorithm": "HS256",                    // ← ALGORITMO
  "expiration_seconds": 3600,              // ← DURACIÓN SELECCIONADA
  "created_at": 1700680000,                // ← FECHA CREACIÓN
  "expires_at": 1700683600,                // ← TIMESTAMP EXPIRACIÓN
  "type": "created",
  "notes": "Token creado con algoritmo HS256 y expiración en 3600s"
}
```

---

## 🔄 FLUJO COMPLETO

```
┌─────────────────────────────────────────────────────────────┐
│ CREAR TOKEN                                                 │
│                                                             │
│ 1. Selecciona algoritmo (HS256 o HS384)                   │
│ 2. Selecciona duración (5 min - 30 días)                  │
│ 3. Ingresa payload JSON                                    │
│ 4. Ingresa secret                                          │
│ 5. Clic en "Crear Token JWT"                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ BACKEND (app.py)                                            │
│                                                             │
│ - Agrega iat: now                                           │
│ - Agrega exp: now + duracion_segundos                      │
│ - Crea header con algoritmo seleccionado                   │
│ - Codifica con encode_jwt()                                │
│ - Guarda en MongoDB con timestamps                         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND (index_improved.html)                              │
│                                                             │
│ ⏳ Temporizador de expiración:                              │
│    - Lee expires_at del servidor                           │
│    - Calcula diferencia con tiempo actual                  │
│    - Actualiza cada 1 segundo                              │
│    - Cambia color: azul → naranja → rojo                  │
│    - Muestra: "⏰ EXPIRADO" cuando llega a 0               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 EJEMPLO PASO A PASO

### Crear token con HS384 que expire en 5 minutos

**1. Selecciona HS384:**
```
Algoritmo: [HS384 (SHA-384)]
```

**2. Selecciona 5 minutos:**
```
Expiración: [5 minutos]
```

**3. Payload:**
```json
{
  "user_id": "12345",
  "role": "admin"
}
```

**4. Secret:**
```
MySecureSecret2024!
```

**5. Clic en "Crear Token JWT"**

**Resultado:**
```
✅ Token creado exitosamente

⏳ 4m 59s
   (Color naranja porque es menos de 5 minutos)

Algoritmo: HS384
Guardado en BD: ✓ SÍ

Tu nuevo JWT:
eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzNDUiLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3MDA2ODA5MDAsImV4cCI6MTcwMDY4MTIwMH0.SIGNATURE...
```

---

## 📊 ALGORITMOS SOPORTADOS

| Algoritmo | Tipo | Tamaño Hash | Uso |
|-----------|------|------------|-----|
| **HS256** | HMAC-SHA256 | 256 bits | Recomendado para la mayoría |
| **HS384** | HMAC-SHA384 | 384 bits | Mayor seguridad |

---

## ⏱️ OPCIONES DE EXPIRACIÓN

| Opción | Segundos | Uso |
|--------|----------|-----|
| 5 minutos | 300 | Testing |
| 10 minutos | 600 | Testing |
| 30 minutos | 1,800 | Sesiones cortas |
| **1 hora** | 3,600 | ← Defecto |
| 24 horas | 86,400 | Sesiones |
| 7 días | 604,800 | Refresh tokens |
| 30 días | 2,592,000 | Tokens de larga duración |

---

## 🎬 PARA LA SUSTENTACIÓN

**Guión de 2 minutos:**

> "Ahora voy a crear un token con expiración configurableE. 
> 
> Como ven, en la pestaña 'Crear Token' tengo:
> - Selector de algoritmo: HS256 o HS384
> - Selector de expiración: desde 5 minutos hasta 30 días
>
> Voy a seleccionar HS384 con 1 hora de expiración.
>
> Ingreso el payload y el secret... y creo el token.
>
> Observen que aparece un temporizador en vivo que muestra exactamente cuánto tiempo queda antes de que expire.
>
> El temporizador se actualiza cada segundo y el token se guarda en MongoDB con todos los timestamps de creación y expiración.
>
> Si esperamos hasta que expire el temporizador, el token se marca como 'EXPIRADO'."

---

## 🔍 VALIDACIÓN

Para verificar que el token fue guardado correctamente en MongoDB con la expiración:

```bash
# 1. Abre MongoDB Compass o mongosh
# 2. Conecta a tu Atlas cluster
# 3. Navega a: jwt_analyzer > tokens
# 4. Busca el token recién creado
# 5. Verifica que tenga:
#    - "expires_at": timestamp
#    - "expiration_seconds": 3600 (o el valor que seleccionaste)
#    - "algorithm": "HS256" o "HS384"
```

---

## ✅ CHECKLIST: TODO IMPLEMENTADO

- [x] Selector de algoritmo en formulario
- [x] Selector de duración en formulario
- [x] Agregar iat al payload
- [x] Agregar exp al payload
- [x] Crear header con algoritmo dinámico
- [x] Guardar algorithm en MongoDB
- [x] Guardar expiration_seconds en MongoDB
- [x] Guardar created_at en MongoDB
- [x] Guardar expires_at en MongoDB
- [x] Temporizador en HTML/JavaScript
- [x] Actualizar temporizador cada segundo
- [x] Cambiar color según tiempo restante
- [x] Mostrar estado "EXPIRADO" cuando llega a 0
- [x] Indicar si está guardado en BD

---

## 🚀 PRÓXIMOS PASOS (OPCIONAL)

1. **API Endpoint para listar tokens por tiempo restante**
   ```
   GET /api/tokens/expiring-soon?minutes=5
   ```

2. **Renovación automática de tokens**
   ```
   POST /api/tokens/{id}/refresh
   ```

3. **Alertas cuando token está a punto de expirar**
   ```
   Sistema de notificaciones
   ```

4. **Blacklist de tokens expirados**
   ```
   Mantener registro de tokens invalidados
   ```

---

**¡Sistema completamente operativo!** 🎉

