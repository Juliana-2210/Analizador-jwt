#!/usr/bin/env python3
"""
Script para configurar y probar la conexión a MongoDB Atlas
"""

import os
import sys
from pathlib import Path

def setup_env():
    """Configura el archivo .env con la cadena de conexión"""
    
    print("=" * 70)
    print("  CONFIGURADOR DE MONGODB ATLAS - JWT ANALYZER")
    print("=" * 70)
    print()
    
    env_file = Path(".env")
    
    print("📋 Instrucciones:")
    print("1. Ve a MongoDB Atlas Dashboard")
    print("2. Haz clic en 'Connect' en tu cluster")
    print("3. Selecciona 'Drivers' → 'Python'")
    print("4. Copia la cadena de conexión (se verá así):")
    print("   mongodb+srv://usuario:contraseña@cluster.mongodb.net/?appName=...")
    print()
    
    # Solicitar la cadena de conexión
    uri = input("🔗 Pega tu cadena de conexión de MongoDB: ").strip()
    
    if not uri.startswith("mongodb+srv://"):
        print("❌ Error: La cadena debe comenzar con 'mongodb+srv://'")
        sys.exit(1)
    
    if "<db_password>" in uri:
        print()
        print("⚠️  Detecté que tu cadena aún tiene '<db_password>'")
        print("Necesitas reemplazarlo con tu contraseña real")
        
        password = input("🔐 ¿Cuál es tu contraseña de MongoDB? ").strip()
        
        if not password:
            print("❌ Error: La contraseña no puede estar vacía")
            sys.exit(1)
        
        uri = uri.replace("<db_password>", password)
        print("✅ Contraseña reemplazada")
    
    # Crear el contenido del .env
    env_content = f"""# MongoDB Atlas Configuration
MONGODB_URI={uri}

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Application Settings
SECRET_KEY=jwt-analyzer-secret-key-2025

"""
    
    # Guardar el archivo .env
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print()
    print("✅ Archivo .env creado exitosamente")
    print()
    
    # Sugerir próximos pasos
    print("=" * 70)
    print("📝 PRÓXIMOS PASOS:")
    print("=" * 70)
    print()
    print("1. Verifica tu conexión:")
    print("   python check_mongodb.py")
    print()
    print("2. Inicia la aplicación:")
    print("   python app.py")
    print()
    print("3. Abre en tu navegador:")
    print("   http://localhost:5000")
    print()
    print("=" * 70)

if __name__ == "__main__":
    try:
        setup_env()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuración cancelada")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
