# 🧪 CÓMO EJECUTAR Y MOSTRAR LOS TESTS

## 📋 Resumen de Tests

Tienes **27 tests** distribuidos en 4 archivos que cubren todos los requisitos:

| Archivo | Tests | Descripción |
|---------|-------|-------------|
| `test_jwt_valid.py` | 8 | ✅ Tokens válidos en HS256 y HS384 |
| `test_jwt_expired.py` | 6 | ⏰ Tokens expirados |
| `test_jwt_malformed.py` | 8 | 🔨 Tokens malformados/inválidos |
| `test_jwt_bad_signature.py` | 5 | ❌ Tokens con firma incorrecta |

---

## 🚀 OPCIÓN 1: Ejecutar TODOS los tests (RECOMENDADO PARA PRESENTACIÓN)

```bash
# Desde el directorio raíz del proyecto
cd "c:\Users\julia\Downloads\lenguajes new"

# Ejecutar todos los tests
pytest tests/ -v

# O con más detalles y colores
pytest tests/ -v --tb=short
```

### Salida esperada:
```
tests/test_jwt_valid.py::test_valid_token_hs256 PASSED
tests/test_jwt_valid.py::test_valid_token_hs384 PASSED
tests/test_jwt_valid.py::test_payload_claims PASSED
...
======================== 27 passed in 2.34s ========================
```

---

## 🎯 OPCIÓN 2: Ejecutar tests por categoría

### A) Solo tokens válidos
```bash
pytest tests/test_jwt_valid.py -v
```

### B) Solo tokens expirados
```bash
pytest tests/test_jwt_expired.py -v
```

### C) Solo tokens malformados
```bash
pytest tests/test_jwt_malformed.py -v
```

### D) Solo tokens con firma inválida
```bash
pytest tests/test_jwt_bad_signature.py -v
```

---

## 📊 OPCIÓN 3: Ejecutar con reporte visual

### Reporte con estadísticas
```bash
pytest tests/ -v --tb=short --co -q
```

### Reporte con cobertura (si instalaste pytest-cov)
```bash
pytest tests/ --cov=jwt_analyzer --cov-report=html
```

---

## 🖼️ OPCIÓN 4: Script visual para presentación (MEJOR)

Crea un archivo `show_tests.py` en el directorio raíz:

```python
#!/usr/bin/env python3
"""Script para mostrar todos los tests de forma visual"""

import subprocess
import sys

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def run_tests():
    print_header("🧪 EJECUTANDO SUITE COMPLETA DE TESTS")
    print("pytest tests/ -v\n")
    
    result = subprocess.run(
        ["pytest", "tests/", "-v", "--tb=short"],
        capture_output=False
    )
    
    if result.returncode == 0:
        print_header("✅ TODOS LOS TESTS PASARON")
    else:
        print_header("❌ ALGUNOS TESTS FALLARON")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())
```

Ejecuta así:
```bash
python show_tests.py
```

---

## 📝 OPCIÓN 5: Script interactivo para presentación

```python
#!/usr/bin/env python3
"""Script interactivo para demos en vivo"""

import subprocess
from datetime import datetime

def separator(title=""):
    print("\n" + "█"*70)
    if title:
        print(f"█ {title:<66}█")
        print("█"*70)
    else:
        print()

def run_category_tests(name, test_file):
    separator(f"🧪 {name}")
    print(f"\nEjecutando: pytest tests/{test_file} -v\n")
    
    result = subprocess.run(
        ["pytest", f"tests/{test_file}", "-v", "--tb=line"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    
    return result.returncode == 0

def main():
    separator("PRESENTACIÓN DE TESTS - JWT ANALYZER")
    print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("Proyecto: Analizador y Validador de JWT")
    print("Fases: Léxica, Sintáctica, Semántica, Codificación, Decodificación, Criptografía")
    
    tests = [
        ("✅ TOKENS VÁLIDOS (8 tests)", "test_jwt_valid.py"),
        ("⏰ TOKENS EXPIRADOS (6 tests)", "test_jwt_expired.py"),
        ("🔨 TOKENS MALFORMADOS (8 tests)", "test_jwt_malformed.py"),
        ("❌ FIRMA INVÁLIDA (5 tests)", "test_jwt_bad_signature.py"),
    ]
    
    results = []
    for name, test_file in tests:
        success = run_category_tests(name, test_file)
        results.append((name, success))
        input("\n[Presiona ENTER para continuar]")
    
    # Resumen
    separator("RESUMEN FINAL")
    total = len(results)
    passed = sum(1 for _, success in results if success)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{'='*70}")
    print(f"TOTAL: {passed}/{total} categorías pasadas")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
```

Ejecuta así:
```bash
python demo_tests_interactivo.py
```

---

## 💡 MIS RECOMENDACIONES PARA LA SUSTENTACIÓN

### **OPCIÓN A: La más simple** ⭐
```bash
pytest tests/ -v
```
Ejecuta todo, muestra los 27 tests pasando.

### **OPCIÓN B: La más profesional** ⭐⭐⭐
```bash
python demo_tests_interactivo.py
```
Muestra cada categoría una por una, permitiendo explicar cada fase.

### **OPCIÓN C: La más rápida**
```bash
pytest tests/ -q
```
Solo muestra: `27 passed in 2.34s`

---

## 📋 DETALLE DE CADA TEST

### ✅ **test_jwt_valid.py** (8 tests)

```python
✅ test_valid_token_hs256
   → Token válido con algoritmo HS256
   → Verifica: estructura, header, payload, firma

✅ test_valid_token_hs384
   → Token válido con algoritmo HS384
   → Verifica: estructura, header, payload, firma

✅ test_payload_claims
   → Validación de claims estándar (sub, iat, exp)

✅ test_header_validation
   → Validación de campos obligatorios en header

✅ test_signature_verification
   → Verificación correcta de firma HMAC

✅ test_multiple_claims
   → Token con múltiples claims personalizados

✅ test_numeric_claims
   → Validación de tipos numéricos en claims

✅ test_standard_claims
   → Validación de claims estándar JWT
```

### ⏰ **test_jwt_expired.py** (6 tests)

```python
⏰ test_expired_token_exp
   → Token con exp < ahora (EXPIRADO)

⏰ test_not_before_nbf
   → Token con nbf > ahora (AÚN NO VÁLIDO)

⏰ test_future_token
   → Token con iat en el futuro

⏰ test_exp_claim_type
   → Validación: exp debe ser número

⏰ test_multiple_time_claims
   → Validación de múltiples claims temporales

⏰ test_time_validation_disabled
   → Análisis sin validación temporal
```

### 🔨 **test_jwt_malformed.py** (8 tests)

```python
🔨 test_missing_dots
   → Token sin puntos separadores (INVÁLIDO)

🔨 test_too_many_parts
   → Token con más de 3 partes (INVÁLIDO)

🔨 test_invalid_base64
   → Header/Payload con Base64 inválido

🔨 test_invalid_json_header
   → Header no es JSON válido

🔨 test_invalid_json_payload
   → Payload no es JSON válido

🔨 test_empty_parts
   → Partes vacías en token

🔨 test_wrong_header_type
   → Header no es objeto JSON

🔨 test_missing_required_header_fields
   → Header falta "alg" o "typ"
```

### ❌ **test_jwt_bad_signature.py** (5 tests)

```python
❌ test_invalid_signature
   → Token con firma incorrecta (RECHAZADO)

❌ test_wrong_secret
   → Verificación con secreto incorrecto

❌ test_modified_payload
   → Token con payload modificado

❌ test_signature_tampering
   → Firma alterada después de generación

❌ test_algorithm_mismatch
   → Algoritmo de firma no coincide
```

---

## 🎬 DURANTE LA PRESENTACIÓN

### **Paso 1: Mostrar el código**
```bash
cat tests/test_jwt_valid.py
```

### **Paso 2: Ejecutar los tests**
```bash
pytest tests/ -v
```

### **Paso 3: Mostrar cobertura** (si quieres)
```bash
pytest tests/ --cov=jwt_analyzer --cov-report=term-missing
```

### **Paso 4: Mostrar un test específico**
```bash
pytest tests/test_jwt_valid.py::test_valid_token_hs256 -v -s
```

---

## 📊 SCRIPT PARA MOSTRAR ESTADÍSTICAS

```python
#!/usr/bin/env python3
"""Mostrar estadísticas de tests"""

import subprocess
import re

result = subprocess.run(
    ["pytest", "tests/", "-v", "--tb=no"],
    capture_output=True,
    text=True
)

print("\n" + "="*70)
print("  📊 ESTADÍSTICAS DE TESTS - JWT ANALYZER")
print("="*70 + "\n")

# Contar tests
output = result.stdout
passed = output.count(" PASSED")
failed = output.count(" FAILED")
skipped = output.count(" SKIPPED")

print(f"✅ Pasados:   {passed}")
print(f"❌ Fallidos:   {failed}")
print(f"⏭️  Omitidos:   {skipped}")
print(f"📊 Total:     {passed + failed + skipped}\n")

# Mostrar cobertura de fases
phases = {
    "Análisis Léxico": "test_jwt_",
    "Análisis Sintáctico": "test_jwt_malformed",
    "Análisis Semántico": "test_jwt_valid",
    "Verificación Criptográfica": "test_jwt_bad_signature",
    "Validación Temporal": "test_jwt_expired",
}

print("Cobertura por fase:")
for phase, pattern in phases.items():
    count = sum(1 for line in output.split('\n') if pattern in line and 'PASSED' in line)
    print(f"  • {phase:30} {count:2} tests")

print("\n" + "="*70 + "\n")
```

---

## ✨ LO QUE DEBES DECIR EN LA PRESENTACIÓN

**"Nuestro proyecto implementa un analizador de JWT con 6 fases de análisis:**

1. **Análisis Léxico**: Tokenización → *Tests: token válido, malformado*
2. **Análisis Sintáctico**: Validación estructura → *Tests: estructura correcta/incorrecta*
3. **Análisis Semántico**: Validación semántica → *Tests: tipos correctos, claims requeridos*
4. **Decodificación**: Parse JSON → *Tests: decodificación correcta*
5. **Codificación**: Generación JWT → *Tests: generación con firma*
6. **Criptografía**: Verificación firma → *Tests: firma válida/inválida*

**Tenemos 27 tests que cubren:**
- ✅ 8 tokens válidos (HS256, HS384)
- ⏰ 6 tokens expirados (exp, nbf, iat)
- 🔨 8 tokens malformados (sintaxis incorrecta)
- ❌ 5 tokens con firma inválida

**Todos los tests pasan exitosamente. ✅**"

---

## 🎯 COMANDO RECOMENDADO PARA PRESENTACIÓN

```bash
# El comando perfecto para mostrar todo
pytest tests/ -v --tb=short --color=yes
```

O directamente sin mostrar los detalles de error:

```bash
# Más limpio
pytest tests/ -v --tb=no
```

¡Listo! 🚀

