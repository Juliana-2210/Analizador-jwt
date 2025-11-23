# 🚀 GUÍA DE EJECUCIÓN - JWT Analyzer

## ⚡ INICIO RÁPIDO (2 minutos)

```bash
# 1. Abre PowerShell en la carpeta del proyecto
cd "c:\Users\julia\Downloads\lenguajes new"

# 2. Inicia el servidor
python app.py

# 3. Abre en el navegador
http://localhost:5000
```

**¡Listo! ✅ La aplicación está corriendo**

---

## 📋 REQUISITOS

- ✅ Python 3.11
- ✅ MongoDB Atlas (conectado)
- ✅ Navegador moderno (Chrome, Firefox, Edge)
- ✅ Archivo `.env` configurado

---

## 🔧 CONFIGURACIÓN INICIAL (Primera vez)

### 1. Crear archivo `.env`

```bash
# En la carpeta principal, crea: .env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Verificar conexión

```bash
python check_mongodb.py
# Deberías ver: ✅ Conectado a MongoDB Atlas
```

---

## 🎯 FUNCIONALIDADES PRINCIPALES

### 📊 ANALIZAR TOKEN

**Ubicación:** Pestaña "📊 Analizar Token"

```
1. Ingresa un token JWT
2. (Opcional) Ingresa el secret
3. Clic en "Analizar Token Completo"
4. Verás 6 fases de análisis:
   ✓ Fase 1: Análisis Léxico
   ✓ Fase 2: Análisis Sintáctico
   ✓ Fase 3: Decodificación Base64URL
   ✓ Fase 4: Análisis Semántico
   ✓ Fase 5: Verificación de Firma
   ✓ Fase 6: Información de Expiración
```

### ➕ CREAR TOKEN

**Ubicación:** Pestaña "➕ Crear Token"

```
1. Selecciona algoritmo:
   - HS256 (SHA-256)
   - HS384 (SHA-384)

2. Selecciona expiración:
   - 30 segundos
   - 1 minuto
   - 2 minutos
   - 3 minutos
   - 5 minutos
   - 10 minutos (máximo)

3. Ingresa el payload JSON
   Ejemplo:
   {
     "user_id": "12345",
     "name": "John Doe"
   }

4. Ingresa tu secret (clave)

5. Clic en "Crear Token JWT"

6. ¡Verás el temporizador contando!
   ⏳ 9m 55s (en tiempo real)
```

### 🧪 CASOS DE PRUEBA

**Ubicación:** Pestaña "🧪 Casos de Prueba"

```
27 casos predefinidos organizados en:

✅ TOKENS VÁLIDOS (8 casos)
   - Token HS256
   - Token HS384
   - [más...]

⏰ TOKENS EXPIRADOS (6 casos)
   - Token expirado
   - [más...]

🔨 TOKENS MALFORMADOS (8 casos)
   - Sin puntos
   - Demasiadas partes
   - Base64 inválido
   - [más...]

❌ FIRMA INVÁLIDA (5 casos)
   - Firma modificada
   - Secret incorrecto
   - [más...]
```

**Cómo usar:**

```
1. Expande una categoría
2. Haz clic en un caso
3. Verás:
   🔐 Token (con botón copiar)
   🔑 Secret (con botón copiar)
   Descripción
   Resultado esperado

4. Haz clic en "Probar en Analizador"
   → Se llena automáticamente
   → Se ejecuta el análisis automáticamente
   → Ves los resultados inmediatamente
```

---

## 📊 ARCHIVOS CLAVE

| Archivo | Función |
|---------|---------|
| `app.py` | Servidor Flask principal |
| `jwt_analyzer/lexer.py` | Análisis léxico |
| `jwt_analyzer/parser.py` | Análisis sintáctico |
| `jwt_analyzer/semantic.py` | Análisis semántico |
| `jwt_analyzer/encoder.py` | Codificación JWT |
| `jwt_analyzer/crypto_verify.py` | Verificación de firma |
| `jwt_analyzer/mongodb.py` | Conexión a BD |
| `templates/index_improved.html` | Interfaz web |
| `static/styles.css` | Estilos |

---

## 🧪 EJECUTAR PRUEBAS

### Pruebas unitarias
```bash
python -m pytest tests/ -v
# Resultado esperado: 27/27 passed ✅
```

### Prueba de expiración
```bash
python test_expiration_feature.py
# Verifica que todo funciona correctamente
```

### Verificar MongoDB
```bash
python check_mongodb.py
# Verifica conexión a Atlas
```

### Verificar token guardado
```bash
python test_save_token.py
# Verifica que se guardan en la BD
```

---

## 🔧 TROUBLESHOOTING

### Error: "MongoDB no conectado"

```
Solución:
1. Verifica que .env existe y tiene MONGODB_URI
2. Verifica que tienes internet
3. Verifica que tu IP está en whitelist de Atlas
4. Reinicia el servidor: python app.py
```

### Error: "Módulo no encontrado"

```
Solución:
pip install -r requirements.txt
```

### Error: "Puerto 5000 en uso"

```
Solución:
# Windows
Get-Process python | Stop-Process -Force
python app.py

# Macros/Linux
lsof -ti :5000 | xargs kill -9
python app.py
```

### Temporizador no actualiza

```
Solución:
1. Limpia caché: Ctrl+F5
2. Abre consola: F12
3. Verifica que no hay errores JavaScript
4. Recarga la página
```

---

## 🎬 DEMOSTRACIÓN (Para profesores)

### Guión de 3 minutos

```
MINUTO 0-1: Introducción
"Este es mi JWT Analyzer. Un sistema completo para 
 analizar tokens JWT a través de 6 fases formales."

MINUTO 1-2: Crear y Demostrar
"Voy a crear un token con HS384 y 5 minutos.
 Observen cómo aparece el temporizador contando.
 Se guarda en MongoDB con todos los timestamps."
[Mostrar crear y temporizador]

MINUTO 2-3: Casos de Prueba
"Tengo 27 casos organizados en 4 categorías.
 Cuando hago clic en 'Probar', todo se llena 
 automáticamente y se ejecuta el análisis."
[Probar un caso]

"Aquí ven todas las 6 fases de análisis ejecutándose."
```

---

## 📱 URLs ÚTILES

| URL | Función |
|-----|---------|
| `http://localhost:5000/` | Web principal |
| `http://localhost:5000/api/tokens` | Ver tokens guardados |
| `http://localhost:5000/api/test-cases` | Obtener casos de prueba |
| `http://localhost:5000/api/statistics` | Ver estadísticas |

---

## 💾 ESTRUCTURA DE CARPETAS

```
c:\Users\julia\Downloads\lenguajes new\
├── app.py                      (Servidor principal)
├── requirements.txt            (Dependencias)
├── .env                        (Configuración)
├── jwt_analyzer/
│   ├── __init__.py
│   ├── lexer.py               (Análisis léxico)
│   ├── parser.py              (Análisis sintáctico)
│   ├── semantic.py            (Análisis semántico)
│   ├── encoder.py             (Codificación)
│   ├── crypto_verify.py       (Firma)
│   ├── base64url.py           (Base64URL)
│   ├── mongodb.py             (Base de datos)
│   └── utils.py               (Utilidades)
├── templates/
│   └── index_improved.html     (Web interactiva)
├── static/
│   └── styles.css             (Estilos)
├── tests/
│   ├── test_jwt_valid.py
│   ├── test_jwt_expired.py
│   ├── test_jwt_malformed.py
│   └── test_jwt_bad_signature.py
└── [Documentación]
    ├── RESUMEN_FINAL.md
    ├── MEJORAS_IMPLEMENTADAS.md
    ├── NUEVO_SISTEMA_EXPIRACION.md
    └── [más...]
```

---

## ✅ CHECKLIST PRE-SUSTENTACIÓN

Antes de presentar:

- [ ] MongoDB conectado (`python check_mongodb.py`)
- [ ] Servidor corriendo (`python app.py`)
- [ ] Tests pasando (`python -m pytest tests/`)
- [ ] Web accesible (`http://localhost:5000`)
- [ ] Crear token funciona
- [ ] Casos de prueba se cargan
- [ ] Auto-llenar funciona
- [ ] Temporizador actualiza
- [ ] MongoDB guarda datos
- [ ] Todas las 6 fases se muestran

---

## 🎯 DATOS INTERESANTES

### Casos de Prueba
- **Total:** 27 tests
- **Válidos:** 8
- **Expirados:** 6
- **Malformados:** 8
- **Firma inválida:** 5

### Algoritmos
- HS256 (SHA-256)
- HS384 (SHA-384)

### Opciones de Expiración
- 30 segundos a 10 minutos
- Máximo: 10 minutos

### Fases de Análisis
1. Léxico (Tokenización)
2. Sintáctico (Estructura)
3. Decodificación (Base64URL)
4. Semántico (Validación)
5. Firma (Criptografía)
6. Temporal (Expiración)

---

## 📞 COMANDOS RÁPIDOS

```bash
# Iniciar servidor
python app.py

# Ejecutar pruebas
python -m pytest tests/ -v

# Verificar MongoDB
python check_mongodb.py

# Verificar expiración
python test_expiration_feature.py

# Limpiar pycache
Remove-Item -Path .\__pycache__ -Recurse -Force
Remove-Item -Path .\jwt_analyzer\__pycache__ -Recurse -Force

# Ver logs en tiempo real
Get-Content app.log -Wait
```

---

## 🎊 ¡LISTO PARA EMPEZAR!

```bash
cd "c:\Users\julia\Downloads\lenguajes new"
python app.py
```

**Abre:** `http://localhost:5000`

**¡Disfruta tu JWT Analyzer! 🚀**

