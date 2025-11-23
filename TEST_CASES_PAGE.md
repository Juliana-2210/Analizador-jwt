# 🧪 PÁGINA DE CASOS DE PRUEBA

Voy a crear una nueva pestaña en la web que muestre todos los casos de prueba. Aquí te muestro cómo lo haré:

## Estructura

La nueva pestaña tendrá:

1. **Categorías de Tests**
   - ✅ Tokens Válidos (8 tests)
   - ⏰ Tokens Expirados (6 tests)  
   - 🔨 Tokens Malformados (8 tests)
   - ❌ Firma Inválida (5 tests)

2. **Para cada test:**
   - Nombre del test
   - Token de ejemplo
   - Descripción
   - Botón "Probar"

3. **Funcionalidad:**
   - Click en "Probar" → carga el token en el analizador
   - Ejecuta automáticamente el análisis
   - Muestra el resultado esperado

## Tokens para demostración:

### ✅ Token Válido (HS256)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```
Secret: `your-256-bit-secret`

### ⏰ Token Expirado
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjoxNTE2MjM5MDIyfQ.1oPvLPCCGb1jUX5f0n5VVAi_-qWkDhS2PuOv0EgVhWw
```
Este token tiene exp=1516239022 (2018)

### 🔨 Token Malformado (sin puntos)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

### ❌ Firma Inválida (modificada)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.FALSESIGNATURE1234567890
```

---

Se verá así en la web:

```
┌─────────────────────────────────────────┐
│ 🧪 CASOS DE PRUEBA                      │
├─────────────────────────────────────────┤
│ ✅ Tokens Válidos     [8 tests]         │
│ ├─ Token HS256        [Probar]          │
│ ├─ Token HS384        [Probar]          │
│ └─ ...                                  │
│                                          │
│ ⏰ Tokens Expirados   [6 tests]          │
│ ├─ Token Expirado     [Probar]          │
│ └─ ...                                  │
│                                          │
│ 🔨 Tokens Malformados [8 tests]         │
│ ├─ Sin Puntos         [Probar]          │
│ └─ ...                                  │
│                                          │
│ ❌ Firma Inválida     [5 tests]          │
│ ├─ Firma Modificada   [Probar]          │
│ └─ ...                                  │
└─────────────────────────────────────────┘
```

## Implementación técnica

En `app.py` agregaré:
- Diccionario con todos los casos de prueba
- Endpoint que retorna los test cases
- JavaScript para cargar el token y analizarlo

En la plantilla HTML:
- Nueva pestaña "Casos de Prueba"
- Acordeón con categorías
- Botones "Probar" que cargan los tokens

