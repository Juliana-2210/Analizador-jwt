#!/usr/bin/env python3
"""
Script para verificar y configurar la conexión a MongoDB Atlas
"""

import os
from dotenv import load_dotenv

print("=" * 80)
print("JWT ANALYZER - VERIFICACIÓN DE MONGODB ATLAS")
print("=" * 80)

# Cargar variables de entorno
load_dotenv()
mongodb_uri = os.getenv("MONGODB_URI", "").strip()

print("\n📋 ESTADO DE CONFIGURACIÓN:\n")

# Verificar .env
if os.path.exists(".env"):
    print("✅ Archivo .env encontrado")
else:
    print("❌ Archivo .env no encontrado")

# Verificar MONGODB_URI
if mongodb_uri:
    # Mostrar URI oculto por seguridad
    masked_uri = mongodb_uri[:20] + "***" + mongodb_uri[-20:]
    print(f"✅ MONGODB_URI configurada: {masked_uri}")
else:
    print("❌ MONGODB_URI NO configurada")
    print("\n📝 PRÓXIMOS PASOS:")
    print("1. Abre el archivo .env")
    print("2. Reemplaza MONGODB_URI= con tu cadena de conexión de MongoDB Atlas")
    print("3. Guarda el archivo")
    print("4. Ejecuta este script nuevamente")
    exit(1)

# Intentar conectar a MongoDB
print("\n🔗 INTENTANDO CONECTAR A MONGODB...\n")

try:
    from jwt_analyzer.mongodb import mongo
    
    # Intentar conectar
    mongo.connect()
    
    if mongo.is_connected():
        print("✅ CONEXIÓN EXITOSA A MONGODB ATLAS")
        
        # Obtener estadísticas
        try:
            db = mongo.get_db()
            collections = db.list_collection_names()
            token_count = db['tokens'].count_documents({}) if 'tokens' in collections else 0
            
            print("\n📊 ESTADÍSTICAS:")
            print(f"   Total de tokens guardados: {token_count}")
            print(f"   Base de datos: {db.name}")
            print(f"   Colecciones disponibles: {collections if collections else 'ninguna aún (normal en primera conexión)'}")
        except Exception as stats_err:
            print(f"\n   ℹ️  Base de datos sin datos aún (normal en primera conexión)")
            print(f"      Los datos se guardarán cuando analices tu primer token")
    else:
        print("❌ NO se pudo conectar a MongoDB Atlas")
        print("\n📝 SOLUCIÓN:")
        print("1. Verifica que tu MONGODB_URI sea correcta")
        print("2. Comprueba que el cluster esté ejecutándose")
        print("3. Verifica que tu IP esté permitida en Network Access")
        print("4. Revisa el usuario y contraseña")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n📝 SOLUCIÓN:")
    print("1. Instala pymongo: pip install pymongo")
    print("   pip install pymongo")
    print("2. Instala python-dotenv: pip install python-dotenv")
    print("   pip install python-dotenv")
    print("3. Ejecuta este script nuevamente")
    print(f"\n📋 Error técnico: {type(e).__name__}: {str(e)}")

print("\n" + "=" * 80)
print("Para más información, lee: GUIDE_MONGODB.md")
print("=" * 80)
