#!/usr/bin/env python3
"""
Script simplificado para desplegar JWT Analyzer en AWS Elastic Beanstalk
Usa las credenciales configuradas en .env
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def print_step(step_num, message):
    """Imprimir pasos del despliegue con formato"""
    print(f"\n{'='*60}")
    print(f"PASO {step_num}: {message}")
    print('='*60)

def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n▶ Ejecutando: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completado exitosamente")
            if result.stdout:
                print(result.stdout[:500])
            return True
        else:
            print(f"❌ Error en {description}")
            print(result.stderr[:500])
            return False
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def check_aws_cli():
    """Verificar si AWS CLI está instalado"""
    print_step(1, "Verificar AWS CLI")
    result = subprocess.run("aws --version", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ AWS CLI instalado: {result.stdout.strip()}")
        return True
    else:
        print("❌ AWS CLI no está instalado")
        print("Descargalo desde: https://aws.amazon.com/cli/")
        return False

def check_eb_cli():
    """Verificar si EB CLI está instalado"""
    print_step(2, "Verificar Elastic Beanstalk CLI")
    result = subprocess.run("eb --version", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ EB CLI instalado: {result.stdout.strip()}")
        return True
    else:
        print("❌ EB CLI no está instalado")
        print("Instalalo con: pip install awsebcli")
        print("Ejecuta: pip install awsebcli")
        return False

def check_docker():
    """Verificar si Docker está instalado"""
    print_step(3, "Verificar Docker")
    result = subprocess.run("docker --version", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Docker instalado: {result.stdout.strip()}")
        return True
    else:
        print("⚠️  Docker no está instalado (opcional para EB)")
        return False

def configure_aws_credentials():
    """Configurar credenciales de AWS"""
    print_step(4, "Configurar credenciales de AWS")
    
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    
    if not access_key or not secret_key:
        print("❌ Credenciales no encontradas en .env")
        return False
    
    # Configurar credenciales usando AWS CLI
    cmd = f'aws configure set aws_access_key_id {access_key} && aws configure set aws_secret_access_key {secret_key} && aws configure set default.region {region}'
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Credenciales configuradas para región: {region}")
        return True
    else:
        print("❌ Error configurando credenciales")
        print(result.stderr)
        return False

def test_aws_connection():
    """Probar conexión a AWS"""
    print_step(5, "Probar conexión a AWS")
    cmd = "aws sts get-caller-identity"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Conexión a AWS exitosa")
        data = json.loads(result.stdout)
        print(f"   Account: {data.get('Account')}")
        print(f"   UserId: {data.get('UserId')}")
        return True
    else:
        print("❌ No se pudo conectar a AWS")
        print(result.stderr)
        return False

def initialize_eb():
    """Inicializar Elastic Beanstalk"""
    print_step(6, "Inicializar Elastic Beanstalk")
    
    app_name = "jwt-analyzer"
    
    # Verificar si ya existe
    result = subprocess.run("eb list", shell=True, capture_output=True, text=True, cwd=os.getcwd())
    
    if result.returncode != 0:
        print(f"Inicializando aplicación: {app_name}")
        cmd = f'eb init -p "Python 3.11 running on 64bit Amazon Linux 2" {app_name} --region us-east-1'
        if not run_command(cmd, "Inicialización de EB"):
            return False
    else:
        print(f"✅ EB ya está inicializado: {result.stdout.strip()}")
    
    return True

def create_eb_environment():
    """Crear entorno en Elastic Beanstalk"""
    print_step(7, "Crear entorno en Elastic Beanstalk")
    
    env_name = "jwt-analyzer-prod"
    
    # Verificar si el entorno ya existe
    result = subprocess.run(f"eb list | findstr {env_name}", shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Entorno ya existe: {env_name}")
        return True
    
    print(f"Creando entorno: {env_name}")
    cmd = f'eb create {env_name} --instance-type t3.micro --envvars MONGODB_URI="{os.getenv("MONGODB_URI")}",FLASK_ENV=production'
    
    if run_command(cmd, "Creación de entorno EB"):
        return True
    else:
        print("⚠️  Puede que el entorno esté siendo creado en background...")
        return True

def deploy_to_eb():
    """Desplegar aplicación a EB"""
    print_step(8, "Desplegar aplicación a Elastic Beanstalk")
    
    # Asegurarse de que los archivos estén listos
    files_to_check = [".ebextensions/python.config", "Dockerfile", "app.py"]
    
    for file in files_to_check:
        if not os.path.exists(file):
            print(f"⚠️  Archivo faltante: {file}")
    
    cmd = "eb deploy"
    if run_command(cmd, "Despliegue"):
        return True
    else:
        return False

def show_deployment_info():
    """Mostrar información del despliegue"""
    print_step(9, "Información del despliegue")
    
    print("\n📊 Estado del entorno:")
    run_command("eb status", "Estado")
    
    print("\n📱 URL de la aplicación:")
    result = subprocess.run("eb open --print-url", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {result.stdout.strip()}")
    
    print("\n📋 Logs recientes:")
    run_command("eb logs --stream", "Logs")

def main():
    """Función principal"""
    print("\n" + "="*60)
    print("🚀 DESPLIEGUE DE JWT ANALYZER EN AWS")
    print("="*60)
    
    # Verificar requisitos previos
    if not check_aws_cli():
        print("\n❌ Por favor instala AWS CLI primero")
        sys.exit(1)
    
    if not check_eb_cli():
        print("\n⚠️  Instalando AWS EB CLI...")
        run_command("pip install awsebcli", "Instalación de EB CLI")
    
    check_docker()
    
    # Configurar y conectar a AWS
    if not configure_aws_credentials():
        sys.exit(1)
    
    if not test_aws_connection():
        sys.exit(1)
    
    # Inicializar y desplegar
    if not initialize_eb():
        print("⚠️  Continuando con el despliegue...")
    
    if not create_eb_environment():
        print("⚠️  Hubo un problema creando el entorno")
    
    if not deploy_to_eb():
        print("⚠️  Hubo un problema con el despliegue")
    
    # Mostrar información final
    show_deployment_info()
    
    print("\n" + "="*60)
    print("✅ ¡DESPLIEGUE COMPLETADO!")
    print("="*60)
    print("\n📝 Próximos pasos:")
    print("1. Abre: eb open")
    print("2. Verifica los logs: eb logs --stream")
    print("3. Para detener: eb terminate jwt-analyzer-prod")
    print("\n")

if __name__ == "__main__":
    main()
