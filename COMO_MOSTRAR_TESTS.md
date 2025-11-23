# 🎬 CÓMO MOSTRAR LOS TESTS EN LA SUSTENTACIÓN

## 📊 Resumen Rápido

Tienes **27 tests** completamente implementados y funcionando. Aquí te muestro cómo ejecutarlos:

---

## 🚀 OPCIÓN 1: La más simple (RECOMENDADA)

```powershell
# Opción A: Ejecutar directamente con pytest
pytest tests/ -v

# Opción B: Usar el script (más limpio)
python run_all_tests.py
```

**Resultado esperado:**
```
tests/test_jwt_valid.py::test_valid_token_hs256 PASSED
tests/test_jwt_valid.py::test_valid_token_hs384 PASSED
tests/test_jwt_valid.py::test_payload_claims PASSED
...
======================== 27 passed in 2.34s ========================
```

---

## 🎯 OPCIÓN 2: Demostración interactiva (MÁS PROFESIONAL)

```powershell
python demo_tests.py demo
```

Te mostrará:
- ✅ Cada fase del analizador
- ✅ Cada categoría de tests
- ✅ Detalles de cada test
- ✅ Permite parar y explicar entre pruebas

---

## 📈 OPCIÓN 3: Modo detallado (Por categoría)

```powershell
python demo_tests.py detailed
```

Ejecuta categoría por categoría:
- ✅ TOKENS VÁLIDOS (8 tests)
- ⏰ TOKENS EXPIRADOS (6 tests)
- 🔨 TOKENS MALFORMADOS (8 tests)
- ❌ FIRMA INVÁLIDA (5 tests)

---

## ⚡ OPCIÓN 4: Pruebas rápidas individuales

### Ver solo tokens válidos
```powershell
pytest tests/test_jwt_valid.py -v
```

### Ver solo tokens expirados
```powershell
pytest tests/test_jwt_expired.py -v
```

### Ver solo tokens malformados
```powershell
pytest tests/test_jwt_malformed.py -v
```

### Ver solo tokens con firma inválida
```powershell
pytest tests/test_jwt_bad_signature.py -v
```

---

## 📋 DETALLES DE LOS TESTS

### ✅ **test_jwt_valid.py** (8 tests)
```python
✓ test_valid_token_hs256          → Token válido HS256
✓ test_valid_token_hs384          → Token válido HS384
✓ test_payload_claims             → Validación de claims
✓ test_header_validation          → Validación de header
✓ test_signature_verification     → Verificación de firma
✓ test_multiple_claims            → Múltiples claims
✓ test_numeric_claims             → Tipos numéricos
✓ test_standard_claims            → Claims estándar JWT
```

### ⏰ **test_jwt_expired.py** (6 tests)
```python
✓ test_expired_token_exp          → Token expirado (exp)
✓ test_not_before_nbf             → Token no válido aún (nbf)
✓ test_future_token               → Token en futuro (iat)
✓ test_exp_claim_type             → Validación tipo exp
✓ test_multiple_time_claims       → Múltiples claims temporales
✓ test_time_validation_disabled   → Sin validación temporal
```

### 🔨 **test_jwt_malformed.py** (8 tests)
```python
✓ test_missing_dots               → Faltan puntos separadores
✓ test_too_many_parts             → Demasiadas partes
✓ test_invalid_base64             → Base64 inválido
✓ test_invalid_json_header        → JSON header inválido
✓ test_invalid_json_payload       → JSON payload inválido
✓ test_empty_parts                → Partes vacías
✓ test_wrong_header_type          → Header no es objeto
✓ test_missing_required_header_fields → Falta "alg" o "typ"
```

### ❌ **test_jwt_bad_signature.py** (5 tests)
```python
✓ test_invalid_signature          → Firma incorrecta
✓ test_wrong_secret               → Secreto incorrecto
✓ test_modified_payload           → Payload modificado
✓ test_signature_tampering        → Firma alterada
✓ test_algorithm_mismatch         → Algoritmo no coincide
```

---

## 🎤 QUÉ DECIR DURANTE LA PRESENTACIÓN

### Introducción:
> "Nuestro proyecto implementa un analizador completo de JWT con 6 fases de análisis formal según los temas del curso de Lenguajes Formales."

### Al ejecutar los tests:
> "Tenemos 27 tests que cubren todos los casos de prueba requeridos:
> - 8 tests de tokens válidos (HS256 y HS384)
> - 6 tests de tokens expirados (validación temporal)
> - 8 tests de tokens malformados (errores sintácticos)
> - 5 tests de tokens con firma inválida (criptografía)
> 
> Todos los tests están implementados y pasando correctamente."

### Explicar cada fase:
```
1️⃣  ANÁLISIS LÉXICO
    → Tokenización y reconocimiento de delimitadores (.)
    → Validación de Base64URL
    → Tests: test_jwt_valid.py y test_jwt_malformed.py

2️⃣  ANÁLISIS SINTÁCTICO  
    → Validación de estructura: HEADER.PAYLOAD.SIGNATURE
    → Parser descendente
    → Tests: test_jwt_malformed.py

3️⃣  ANÁLISIS SEMÁNTICO
    → Validación de campos obligatorios (alg, typ, etc)
    → Validación de tipos de datos
    → Validación de claims
    → Tests: test_jwt_valid.py y test_jwt_expired.py

4️⃣  DECODIFICACIÓN
    → Parser JSON para header y payload
    → Extracción Base64URL
    → Tests: test_jwt_valid.py

5️⃣  CODIFICACIÓN
    → Generación de JWT
    → Firma HMAC
    → Tests: test_jwt_valid.py

6️⃣  CRIPTOGRAFÍA
    → Verificación de firma HMAC
    → Comparación timing-safe
    → Tests: test_jwt_bad_signature.py
```

---

## 🎯 MI RECOMENDACIÓN PARA LA SUSTENTACIÓN

### **Paso 1: Mostrar los tests en ejecución** (2 minutos)
```powershell
pytest tests/ -v
```

### **Paso 2: Explicar cada categoría** (5 minutos)
```powershell
# Mostrar y explicar cada categoría
pytest tests/test_jwt_valid.py -v --tb=no
pytest tests/test_jwt_malformed.py -v --tb=no
pytest tests/test_jwt_expired.py -v --tb=no
pytest tests/test_jwt_bad_signature.py -v --tb=no
```

### **Paso 3: Mostrar un test específico** (2 minutos)
```powershell
# Ejecutar un test con output completo
pytest tests/test_jwt_valid.py::test_valid_token_hs256 -v -s
```

### **Paso 4: Mostrar la aplicación web** (3 minutos)
```powershell
# Iniciar servidor
python app.py

# Abrir http://localhost:5000
# Demostrar análisis en tiempo real
# Mostrar datos guardándose en MongoDB
```

---

## 💡 TIPS PARA LA PRESENTACIÓN

✅ **DO:**
- Ejecuta los tests en vivo
- Muestra el código de un test simple
- Explica qué valida cada test
- Demuestra que todos pasan

❌ **DON'T:**
- No ejecutes tests en background
- No hables muy rápido
- No muestres demasiado código a la vez
- No olvides pausar entre demostraciones

---

## 📝 GUIÓN SUGERIDO

```
Profesor: "¿Puedes mostrar tus tests?"

Tú: "Por supuesto. Tengo 27 tests implementados 
que validan todas las fases del analizador."

[Ejecuta: pytest tests/ -v]

"Como ves, tenemos:
- 8 tests para tokens válidos
- 6 tests para tokens expirados  
- 8 tests para tokens malformados
- 5 tests para verificación de firma

Todos están pasando correctamente. ✅

¿Quieres que muestre un test específico?"

Profesor: "Sí, muestra el de tokens válidos"

[Ejecuta: pytest tests/test_jwt_valid.py -v]

"Aquí vemos 8 tests que validan:
- Estructura correcta
- Header válido
- Payload válido
- Firma correcta
- Claims estándar
- Múltiples algoritmos

Todos validan la integridad del token completo."
```

---

## 🎬 ARCHIVOS LISTOS PARA USAR

✅ `RUN_TESTS.md` - Documentación completa
✅ `run_all_tests.py` - Script simple para ejecutar
✅ `demo_tests.py` - Script interactivo profesional
✅ `test_jwt_valid.py` - 8 tests de tokens válidos
✅ `test_jwt_expired.py` - 6 tests de tokens expirados
✅ `test_jwt_malformed.py` - 8 tests de tokens malformados
✅ `test_jwt_bad_signature.py` - 5 tests de firma inválida

---

## 🚀 ¡LISTO!

Ahora tienes todo lo que necesitas para mostrar tus tests en la sustentación. 

**Recomendación final:**
Practica 2-3 veces antes de sustentar para que veas cómo se ejecutan y qué tiempo toman. ⏱️

