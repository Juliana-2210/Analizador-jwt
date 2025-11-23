# 🗄️ Guía de Configuración MongoDB Atlas

## 📋 Paso a Paso para Conectar el Proyecto a MongoDB Atlas

### **Paso 1: Crear una Cuenta en MongoDB Atlas**

1. Ve a [https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Haz clic en **"Sign Up"** (o "Registrarse")
3. Crea una cuenta con tu email o usa Google/GitHub
4. Verifica tu email

---

### **Paso 2: Crear un Proyecto**

1. En el dashboard, haz clic en **"Create a Project"**
2. Nombra tu proyecto: `JWT Analyzer`
3. Haz clic en **"Create Project"**

---

### **Paso 3: Crear un Cluster Gratuito**

1. Haz clic en **"Create a Cluster"**
2. Selecciona el plan **FREE** (es gratis)
3. Elige tu proveedor (AWS, Google Cloud, Azure) - mantén el default
4. Elige tu región (la más cercana a ti)
5. Nombra tu cluster: `jwt-analyzer-cluster`
6. Haz clic en **"Create Cluster"**
7. ⏳ Espera 2-3 minutos mientras se crea

---

### **Paso 4: Crear un Usuario de Base de Datos**

1. En el panel del cluster, ve a **"Database Access"** (en el menú izquierdo)
2. Haz clic en **"+ Add Database User"**
3. Elige método: **Password**
4. Username: `jwt_user`
5. Password: `TuContraseñaSegura123!` (cópialo en algún lugar)
6. Haz clic en **"Add User"**

---

### **Paso 5: Permitir Acceso desde tu IP**

1. Ve a **"Network Access"** (en el menú izquierdo)
2. Haz clic en **"+ Add IP Address"**
3. Opción A: **Allow Access from Anywhere** (para desarrollo)
   - Haz clic en "Allow Access from Anywhere"
   - Confirma
   
   Opción B: Agregar tu IP específica
   - Haz clic en "Add IP Address"
   - Copia tu IP pública
   - Pega en "IP Address"

---

### **Paso 6: Obtener la Cadena de Conexión**

1. Ve a tu **Cluster**
2. Haz clic en **"Connect"**
3. Selecciona **"Connect your application"**
4. Elige **Python** y versión **4.0 or later**
5. Copia la cadena de conexión que se muestra:
   ```
   mongodb+srv://jwt_user:TuContraseñaSegura123!@jwt-analyzer-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

---

### **Paso 7: Configurar tu Proyecto**

1. Abre el archivo `.env` en tu proyecto:
   ```
   c:\Users\julia\Downloads\lenguajes new\.env
   ```

2. Reemplaza esto:
   ```
   MONGODB_URI=
   ```
   
   Con la cadena que copiaste:
   ```
   MONGODB_URI=mongodb+srv://jwt_user:TuContraseñaSegura123!@jwt-analyzer-cluster.xxxxx.mongodb.net/jwt_analyzer?retryWrites=true&w=majority
   ```

3. Guarda el archivo

---

### **Paso 8: Instalar Dependencias**

```powershell
cd "c:\Users\julia\Downloads\lenguajes new"
pip install pymongo python-dotenv
```

---

### **Paso 9: Probar la Conexión**

```powershell
python -c "from jwt_analyzer.mongodb import mongo; print('✅ Conectado!' if mongo.is_connected() else '❌ No conectado')"
```

Si ves **"✅ Conectado!"**, ¡perfecto! 🎉

Si ves **"❌ No conectado"**, revisa:
- La cadena de conexión está correcta
- El usuario y contraseña son correctos
- Tu IP está permitida en Network Access

---

## 🚀 Usar MongoDB en la Aplicación

### **Crear y Guardar Tokens**

1. Inicia la app: `python app.py`
2. Abre: `http://localhost:5000`
3. Crea un token
4. Analízalo
5. ✅ Se guarda automáticamente en MongoDB Atlas

### **Ver Tokens Guardados (API REST)**

```bash
# Ver todos los tokens
curl http://localhost:5000/api/tokens

# Ver estadísticas
curl http://localhost:5000/api/statistics

# Ver colecciones
curl http://localhost:5000/api/collections
```

---

## 📚 Operaciones Disponibles

### **Tokens**
- `GET /api/tokens` - Ver todos los tokens
- `POST /api/tokens` - Guardar un token
- `GET /api/tokens/<id>` - Ver un token específico
- `DELETE /api/tokens/<id>` - Eliminar un token

### **Colecciones**
- `GET /api/collections` - Ver todas las colecciones
- `POST /api/collections` - Crear una colección
- `GET /api/collections/<id>` - Ver una colección
- `POST /api/collections/<id>/tokens/<token_id>` - Agregar token a colección
- `DELETE /api/collections/<id>/tokens/<token_id>` - Quitar token de colección
- `DELETE /api/collections/<id>` - Eliminar una colección

---

## 🔒 Seguridad

**IMPORTANTE:** Nunca subas el archivo `.env` a GitHub

Añade esto al `.gitignore`:
```
.env
.env.local
.DS_Store
__pycache__/
*.pyc
venv/
.vscode/
```

---

## 🆘 Solución de Problemas

### Error: "No such module named 'pymongo'"
```powershell
pip install pymongo
```

### Error: "Connection timeout"
1. Revisa que tu IP esté permitida en Network Access
2. Verifica la cadena de conexión
3. Comprueba que el cluster esté ejecutándose

### Error: "Authentication failed"
1. Verifica el usuario y contraseña
2. Crea un nuevo usuario en Database Access

### Error: "Access denied from this IP"
1. Ve a Network Access
2. Agrega tu IP o selecciona "Allow from Anywhere"

---

## 📖 Recursos

- [MongoDB Atlas Docs](https://docs.mongodb.com/atlas/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Query Language](https://docs.mongodb.com/manual/reference/operator/query/)

---

¡Ya está! 🎉 Tu JWT Analyzer está conectado a MongoDB Atlas y guardará todos los tokens analizados.
