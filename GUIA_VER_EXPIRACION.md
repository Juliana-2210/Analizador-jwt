# 🎬 GUÍA PASO A PASO: Ver la Nueva Funcionalidad de Expiración

## Objetivo
Ver en tiempo real cómo el JWT Analyzer muestra si un token está expirado o activo en la parte superior de la página.

---

## 📋 Pasos

### PASO 1: Asegurate que el servidor está corriendo

```powershell
cd "c:\Users\julia\Downloads\lenguajes new"
python app.py
```

**Debe mostrar:**
```
✅ Conectado a MongoDB Atlas
* Running on http://127.0.0.1:5000
```

Si ves esto, el servidor está listo. ✅

---

### PASO 2: Abre el navegador

Abre cualquier navegador (Chrome, Firefox, Edge, etc.) y ve a:

```
http://localhost:5000
```

**Debes ver:** La página principal del JWT Analyzer

---

### PASO 3: Ve a la pestaña "Analizar Token"

En la parte superior, haz clic en:

```
[📊 Analizar Token]
```

**Debes ver:** Un formulario con dos campos:
- Campo de texto para el token
- Campo de texto para el secret

---

### PASO 4: Ingresa un token expirado

Copia y pega este token en el campo del token:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjoxNTE2MjM5MDIyfQ.1oPvLPCCGb1jUX5f0n5VVAi_-qWkDhS2PuOv0EgVhWw
```

---

### PASO 5: Ingresa el secreto

En el campo "Ingresa secreto:", escribe:

```
secret
```

---

### PASO 6: Haz clic en "Analizar Token Completo"

Busca y haz clic en el botón:

```
[Analizar Token Completo]
```

---

### PASO 7: Mira la parte superior

**¡AHORA VES LO NUEVO!** 

En la parte superior de la página, junto con:
- ✓ Análisis Léxico
- ✓ Análisis Sintáctico  
- ✓ Análisis Semántico
- ✓ Firma

**¡Aparece lo nuevo!**

```
┌────────────────────────────────────────┐
│ ⏳ Estado de Expiración               │
│ ✗ Expirado                            │
│ Expiró hace: 5+ años                  │
│ (es un token muy antiguo)             │
└────────────────────────────────────────┘
```

---

## 🎯 Resultado Esperado

### Antes de hacer clic en "Analizar":
```
⏳ Estado de Expiración
Pendiente
```

### Después de hacer clic en "Analizar":
```
⏳ Estado de Expiración
✗ Expirado
Expiró hace: 5+ años
```

---

## 🧪 PRUEBA 2: Token Activo (en 10 minutos)

Ahora prueba con un token que acaba de crearse:

### PASO 1: Ve a "Crear Token"

Haz clic en:
```
[➕ Crear Token]
```

---

### PASO 2: Completa el formulario

```
Ingresa algoritmo: HS256
Ingresa expiración: 10 minutos
Ingresa payload: {"user": "test"}
Ingresa secreto: mysecret
```

---

### PASO 3: Haz clic en "Crear Token JWT"

El servidor genera un token nuevo.

---

### PASO 4: Copia el token

El token nuevo aparece debajo. Cópialo.

---

### PASO 5: Ve de vuelta a "Analizar Token"

Haz clic en:
```
[📊 Analizar Token]
```

---

### PASO 6: Pega el token

```
[Token que acabas de copiar]
```

---

### PASO 7: Ingresa el secreto

```
mysecret
```

---

### PASO 8: Haz clic en "Analizar Token Completo"

---

### PASO 9: Mira la expiración

**¡Ahora verás!**

```
⏳ Estado de Expiración
✓ Activo
Expira en: 9m 58s
```

El tiempo va bajando. ✓

---

## ⏰ OBSERVACIÓN EN VIVO

Si esperas 10 minutos (o creas un token con 30 segundos), verás:

- **Minuto 0:** `Expira en: 30s` (verde ✓)
- **Minuto 0.5:** `Expira en: 0s` (seguía verde)
- **Minuto 1:** `Expiró hace: 0s` (cambió a rojo ✗)

---

## 🎬 Secuencia Visual Completa

```
PASO 1: Servidor corriendo
┌─────────────────────────────┐
│ ✅ Conectado a MongoDB Atlas │
│ ✅ Running on localhost:5000 │
└─────────────────────────────┘

PASO 2-3: Página cargada
┌────────────────────────────────┐
│ [Analizar] [Crear] [Casos]   │
│ ⏳ Pendiente                  │
└────────────────────────────────┘

PASO 4-5: Token y secreto ingresados
┌────────────────────────────────┐
│ Token: eyJhbGciOi...          │
│ Secret: secret                │
│ [Analizar Token Completo]    │
└────────────────────────────────┘

PASO 6-7: ✨ ¡RESULTADO!
┌────────────────────────────────┐
│ ✓ Léxico  ✓ Sintáctico        │
│ ✓ Semántico ✓ Firma           │
│ ⏳ EXPIRACIÓN: ✗ Expirado     │
│    Expiró hace: 5+ años       │
└────────────────────────────────┘
```

---

## ✅ Checklist de Verificación

- [ ] Servidor Flask corriendo en localhost:5000
- [ ] Página cargó sin errores
- [ ] Puedo ver la pestaña "Analizar Token"
- [ ] Ingresé un token y secreto correctamente
- [ ] Hice clic en "Analizar Token Completo"
- [ ] Aparece una nueva sección "Estado de Expiración"
- [ ] El badge muestra ✓ Activo o ✗ Expirado
- [ ] Se muestra el tiempo (Expira en: X o Expiró hace: X)

Si todas las casillas están marcadas: ✅ **¡TODO FUNCIONA!**

---

## 🆘 Troubleshooting

### Error 1: "No puedo conectar a localhost:5000"
**Solución:**
```powershell
# Verifica que el servidor está corriendo
# Terminal 1: Abre una nueva terminal y ejecuta:
cd "c:\Users\julia\Downloads\lenguajes new"
python app.py

# Terminal 2: Luego abre el navegador y prueba de nuevo
http://localhost:5000
```

### Error 2: "No aparece la sección de expiración"
**Solución:**
```
1. Haz clic en "Analizar Token Completo"
2. Espera 2 segundos
3. Recarga la página (Ctrl+R o F5)
4. Si sigue sin aparecer, revisa la consola del navegador (F12)
```

### Error 3: "El token no se analiza"
**Solución:**
```
1. Verifica que el token tenga 3 partes (xxx.yyy.zzz)
2. Verifica que el secreto sea correcto
3. Intenta con un token conocido (de los casos de prueba)
```

---

## 📞 Tokens de Prueba Rápida

### Token Expirado (¡Úsalo primero!)
```
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjoxNTE2MjM5MDIyfQ.1oPvLPCCGb1jUX5f0n5VVAi_-qWkDhS2PuOv0EgVhWw
Secret: secret
Resultado: ✗ Expirado
```

### Token Válido (HS256)
```
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
Secret: your-256-bit-secret
Resultado: ✓ Válido (sin 'exp' o futuro)
```

---

## 🎓 Qué Aprendiste

✅ Cómo crear tokens con expiración  
✅ Cómo analizar tokens en tiempo real  
✅ Cómo ver si un token está activo o expirado  
✅ Cómo entender los claims JWT (especialmente 'exp')  
✅ Cómo el servidor calcula el tiempo restante  

---

## 📚 Archivos Relacionados

Si quieres leer más sobre esto:
- `NUEVA_FUNCIONALIDAD_EXPIRACION.md` - Documentación completa
- `COMPLETADO_EXPIRACION.md` - Resumen técnico
- `UBICACION_EXPIRACION.md` - Dónde aparece en la interfaz
- `app.py` - Backend (líneas ~270-330)
- `templates/index_improved.html` - Frontend (líneas ~25-60)

---

## 🚀 ¡Listo!

Ya sabes cómo usar la nueva funcionalidad de expiración.

**Próximo paso:**
1. Prueba con diferentes tokens
2. Crea tokens con diferentes expiraciones
3. Ve cómo cambia el estado de expiración
4. ¡Enseña a tus compañeros!

---

**Versión:** 1.0  
**Fecha:** Noviembre 23, 2025  
**Status:** ✅ Completado

