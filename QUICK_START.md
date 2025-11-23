# 🎯 INSTRUCCIONES DE MONGODB ATLAS - RESUMEN RÁPIDO

## 1️⃣ OBTENER LA URL DE MONGODB ATLAS

### Opción A: Si ya tienes una cuenta (RECOMENDADO)
1. Ve a https://www.mongodb.com/cloud/atlas
2. Login con tu cuenta
3. Abre tu proyecto **JWT Analyzer**
4. Click en **Clusters**
5. Click en **Connect** → **Connect your application**
6. Selecciona **Python 4.0 or later**
7. COPIA la cadena de conexión (similar a esto):
   ```
   mongodb+srv://jwt_user:TuPassword@jwt-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### Opción B: Crear cuenta nueva (Toma 5 minutos)
Sigue estos pasos en: `GUIDE_MONGODB.md`

---

## 2️⃣ CONFIGURAR EL PROYECTO

Abre el archivo `.env` en la carpeta del proyecto:
```
c:\Users\julia\Downloads\lenguajes new\.env
```

Reemplaza esto:
```
MONGODB_URI=
```

Con tu URL (la que copiaste):
```
MONGODB_URI=mongodb+srv://jwt_user:TuPassword@jwt-cluster.xxxxx.mongodb.net/jwt_analyzer?retryWrites=true&w=majority
```

**Guarda el archivo** (Ctrl+S)

---

## 3️⃣ VERIFICAR LA CONEXIÓN

Abre PowerShell y ejecuta:
```powershell
cd "c:\Users\julia\Downloads\lenguajes new"
python check_mongodb.py
```

Deberías ver: ✅ CONEXIÓN EXITOSA A MONGODB ATLAS

---

## 4️⃣ USAR LA APLICACIÓN

### Iniciar la app:
```powershell
python app.py
```

### Abrir en el navegador:
```
http://localhost:5000
```

### Crear tokens:
1. Ve a pestaña **"Crear Token"**
2. Usa los ejemplos de payloads
3. Haz clic en **"Crear JWT"**
4. ✅ Se guardará automáticamente en MongoDB Atlas

### Analizar tokens:
1. Ve a pestaña **"Analizar Token"**
2. Pega un token
3. Haz clic en **"Analizar Token Completo"**
4. ✅ Se guardará el análisis en MongoDB Atlas

---

## 5️⃣ PROBAR LAS APIS REST

En otra terminal:
```powershell
cd "c:\Users\julia\Downloads\lenguajes new"
python test_api.py
```

Esto probará todos los endpoints:
- Ver tokens guardados
- Ver estadísticas
- Crear colecciones
- Agregar tokens a colecciones

---

## 📊 DATOS GUARDADOS EN MONGODB

### Colección: `tokens`
Cada token guardado contiene:
```json
{
  "_id": "...",
  "token": "eyJ...",
  "header": {"alg": "HS256", "typ": "JWT"},
  "payload": {"sub": "123", "name": "John"},
  "signature": "7sl73...",
  "type": "valid",
  "is_valid": true,
  "signature_valid": true,
  "algorithm": "HS256",
  "analysis": {...},
  "created_at": "2025-11-22T..."
}
```

### Colección: `collections`
Cada colección contiene:
```json
{
  "_id": "...",
  "name": "Mi Colección",
  "description": "Descripción",
  "user_id": "default",
  "tokens": ["id1", "id2", "id3"],
  "created_at": "2025-11-22T...",
  "updated_at": "2025-11-22T..."
}
```

---

## 🔧 TROUBLESHOOTING

### "❌ NO se pudo conectar a MongoDB Atlas"
**Soluciones:**
1. Verifica que la URL en `.env` sea correcta
2. Verifica que el cluster esté ejecutándose en MongoDB Atlas
3. Ve a Network Access en MongoDB Atlas y agrega tu IP
4. Revisa que el usuario y contraseña sean correctos

### "No such module named 'pymongo'"
```powershell
pip install pymongo python-dotenv
```

### La app no inicia
Asegúrate de instalar todas las dependencias:
```powershell
pip install -r requirements.txt
```

---

## 📚 MÁS INFORMACIÓN

- `GUIDE_MONGODB.md` - Guía completa de MongoDB Atlas
- `README_COMPLETO.md` - Documentación del proyecto
- `demo.py` - Demostración de funcionalidades

---

## ✅ CHECKLIST FINAL

- [ ] Tengo una cuenta en MongoDB Atlas
- [ ] He creado un cluster
- [ ] He creado un usuario de DB
- [ ] He permitido mi IP en Network Access
- [ ] Tengo mi cadena de conexión
- [ ] He configurado `.env` con la URL
- [ ] He ejecutado `check_mongodb.py` y veo ✅
- [ ] La app inicia sin errores: `python app.py`
- [ ] Puedo crear y guardar tokens
- [ ] Los datos aparecen en MongoDB Atlas

---

¡Listo! 🎉 Tu JWT Analyzer está completamente integrado con MongoDB Atlas.

**Cualquier duda, ejecuta:**
```powershell
python check_mongodb.py
```

Para verificar la conexión en cualquier momento.
