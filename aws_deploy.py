#!/usr/bin/env python3
"""
Script para preparar y desplegar en AWS
Ejecutar: python aws_deploy.py
"""

import os
import sys
import subprocess
import json

def run_command(cmd, description=""):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n{'='*70}")
    print(f"► {description}")
    print(f"{'='*70}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False)
        if result.returncode == 0:
            print(f"✓ {description} - OK")
            return True
        else:
            print(f"✗ {description} - ERROR")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def check_aws_cli():
    """Verificar si AWS CLI está instalado"""
    print("\n[1/5] Verificando AWS CLI...")
    result = subprocess.run("aws --version", shell=True, capture_output=True)
    if result.returncode == 0:
        print("✓ AWS CLI instalado")
        return True
    else:
        print("✗ AWS CLI NO instalado")
        print("Descargar desde: https://aws.amazon.com/cli/")
        return False

def check_docker():
    """Verificar si Docker está instalado"""
    print("\n[2/5] Verificando Docker...")
    result = subprocess.run("docker --version", shell=True, capture_output=True)
    if result.returncode == 0:
        print("✓ Docker instalado")
        return True
    else:
        print("✗ Docker NO instalado (opcional)")
        return True  # No es obligatorio

def check_eb_cli():
    """Verificar si EB CLI está instalado"""
    print("\n[3/5] Verificando Elastic Beanstalk CLI...")
    result = subprocess.run("eb --version", shell=True, capture_output=True)
    if result.returncode == 0:
        print("✓ EB CLI instalado")
        return True
    else:
        print("✗ EB CLI NO instalado")
        print("Instalando EB CLI...")
        run_command("pip install awsebcli", "Instalando AWS EB CLI")
        return True

def show_menu():
    """Mostrar menú de opciones"""
    print("\n" + "="*70)
    print("DESPLIEGUE EN AWS - SELECCIONA OPCIÓN")
    print("="*70)
    print("\n1. Elastic Beanstalk (Recomendado)")
    print("2. EC2 (Manual)")
    print("3. Lightsail (Simple)")
    print("4. App Runner (Con Docker)")
    print("5. Solo preparar archivos (No desplegar)")
    print("0. Salir")
    
    choice = input("\nSelecciona opción (0-5): ").strip()
    return choice

def deploy_elastic_beanstalk():
    """Desplegar en Elastic Beanstalk"""
    print("\n" + "="*70)
    print("DESPLIEGUE ELASTIC BEANSTALK")
    print("="*70)
    
    app_name = input("\nNombre de la aplicación (ej: jwt-analyzer): ").strip() or "jwt-analyzer"
    region = input("Región AWS (ej: us-east-1): ").strip() or "us-east-1"
    
    print("\n[Paso 1] Inicializando EB...")
    run_command(f"eb init -p python-3.11 {app_name} --region {region}", 
                "Inicializar Elastic Beanstalk")
    
    print("\n[Paso 2] Creando ambiente...")
    env_name = f"{app_name}-env"
    run_command(f"eb create {env_name}", 
                "Crear ambiente EB")
    
    print("\n[Paso 3] Agregando variables de entorno...")
    mongodb_uri = input("\nIngresa tu MONGODB_URI: ").strip()
    if mongodb_uri:
        run_command(f'eb setenv MONGODB_URI="{mongodb_uri}"', 
                    "Configurar MongoDB URI")
    
    print("\n[Paso 4] Desplegando aplicación...")
    run_command("eb deploy", "Desplegar cambios")
    
    print("\n[Paso 5] Abriendo aplicación...")
    run_command("eb open", "Abrir en navegador")
    
    print("\n✓ ¡Despliegue completado!")
    print(f"Aplicación disponible en: http://{env_name}.{region}.elasticbeanstalk.com")

def prepare_docker():
    """Preparar Docker para AWS"""
    print("\n" + "="*70)
    print("PREPARAR DOCKER PARA AWS")
    print("="*70)
    
    print("\n[Paso 1] Verificando Dockerfile...")
    if os.path.exists("Dockerfile"):
        print("✓ Dockerfile encontrado")
    else:
        print("✗ Dockerfile no encontrado")
        return
    
    print("\n[Paso 2] Construyendo imagen Docker...")
    run_command("docker build -t jwt-analyzer:latest .", "Construir imagen Docker")
    
    print("\n[Paso 3] Probando imagen localmente...")
    run_command("docker run -p 5000:5000 jwt-analyzer:latest", "Probar imagen (presiona Ctrl+C para detener)")
    
    print("\nProximos pasos para AWS:")
    print("1. Crear ECR: aws ecr create-repository --repository-name jwt-analyzer")
    print("2. Hacer login: aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com")
    print("3. Tag: docker tag jwt-analyzer:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/jwt-analyzer:latest")
    print("4. Push: docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/jwt-analyzer:latest")

def prepare_files():
    """Solo preparar archivos"""
    print("\n" + "="*70)
    print("PREPARAR ARCHIVOS PARA AWS")
    print("="*70)
    
    files = {
        "requirements.txt": "Dependencias Python",
        "Dockerfile": "Configuración Docker",
        "docker-compose.yml": "Docker Compose para pruebas",
        ".ebextensions/python.config": "Configuración Elastic Beanstalk",
        "start.sh": "Script de inicio",
    }
    
    print("\nArchivos preparados:")
    for file, desc in files.items():
        status = "✓" if os.path.exists(file) else "✗"
        print(f"{status} {file:40} - {desc}")
    
    print("\nArchivos para referencia:")
    print("- DESPLIEGUE_AWS.txt - Guía completa")
    print("- .env.example - Variables de entorno")

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("AWS DEPLOYMENT HELPER - JWT ANALYZER")
    print("="*70)
    
    # Verificaciones iniciales
    if not check_aws_cli():
        print("\n✗ AWS CLI es requerido")
        sys.exit(1)
    
    check_docker()
    check_eb_cli()
    
    # Menú
    while True:
        choice = show_menu()
        
        if choice == "1":
            deploy_elastic_beanstalk()
        elif choice == "2":
            print("\nPara EC2, sigue la guía en DESPLIEGUE_AWS.txt - Opción 2")
        elif choice == "3":
            print("\nPara Lightsail, sigue la guía en DESPLIEGUE_AWS.txt - Opción 3")
        elif choice == "4":
            prepare_docker()
        elif choice == "5":
            prepare_files()
        elif choice == "0":
            print("\n¡Hasta luego!")
            sys.exit(0)
        else:
            print("✗ Opción inválida")
        
        again = input("\n¿Otra operación? (s/n): ").strip().lower()
        if again != "s":
            break
    
    print("\n" + "="*70)
    print("✓ ¡Proceso completado!")
    print("="*70)

if __name__ == "__main__":
    main()
