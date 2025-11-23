#!/usr/bin/env python3
"""
Script interactivo para demostración de tests en la sustentación
Ejecuta: python demo_tests.py
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def separator(title="", char="█"):
    if title:
        padding = (70 - len(title) - 2) // 2
        print(f"\n{char}" + "█" * 70)
        print(f"{char} {title.center(68)} {char}")
        print(f"{char}" + "█" * 70 + "\n")
    else:
        print(f"\n{char}" * 72 + "\n")

def print_phase(emoji, name, description):
    print(f"{emoji} {bcolors.BOLD}{name}{bcolors.ENDC}")
    print(f"   {description}\n")

def run_tests(test_file=None, quiet=False):
    """Ejecutar tests y retornar resultado"""
    cmd = [sys.executable, "-m", "pytest"]
    
    if test_file:
        cmd.append(f"tests/{test_file}")
    else:
        cmd.append("tests/")
    
    cmd.extend(["-v", "--tb=line"])
    
    if quiet:
        cmd.append("-q")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def demo_mode():
    """Modo demostración interactivo"""
    
    separator("🎬 DEMOSTRACIÓN DE TESTS", "═")
    print(f"{bcolors.BOLD}Proyecto: Analizador y Validador de JWT{bcolors.ENDC}")
    print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Curso: Lenguajes Formales 2025-2\n")
    
    separator("FASES DEL ANALIZADOR")
    
    print_phase("1️⃣", "ANÁLISIS LÉXICO", 
                "Tokenización y reconocimiento de delimitadores")
    print_phase("2️⃣", "ANÁLISIS SINTÁCTICO", 
                "Validación de estructura JWT → HEADER.PAYLOAD.SIGNATURE")
    print_phase("3️⃣", "ANÁLISIS SEMÁNTICO", 
                "Validación de campos, tipos, y claims")
    print_phase("4️⃣", "DECODIFICACIÓN", 
                "Extracción de header, payload y claims")
    print_phase("5️⃣", "CODIFICACIÓN", 
                "Generación de nuevos JWT con firma")
    print_phase("6️⃣", "CRIPTOGRAFÍA", 
                "Verificación de firmas HMAC")
    
    input(f"{bcolors.WARNING}[Presiona ENTER para mostrar casos de prueba]{bcolors.ENDC}")
    
    # Casos de prueba
    separator("CASOS DE PRUEBA IMPLEMENTADOS")
    
    test_cases = [
        ("✅ TOKENS VÁLIDOS", 
         "Tokens correctos con algoritmos HS256 y HS384\n   Valida: estructura, claims, firma",
         "test_jwt_valid.py", 8),
        
        ("⏰ TOKENS EXPIRADOS",
         "Validación temporal: exp, iat, nbf\n   Detecta tokens caducados o no válidos aún",
         "test_jwt_expired.py", 6),
        
        ("🔨 TOKENS MALFORMADOS",
         "Errores de sintaxis: puntos faltantes, JSON inválido\n   Estructura incorrecta o partes vacías",
         "test_jwt_malformed.py", 8),
        
        ("❌ FIRMA INVÁLIDA",
         "Verificación criptográfica: firma alterada\n   Detecta modificaciones y secretos incorrectos",
         "test_jwt_bad_signature.py", 5),
    ]
    
    for title, desc, test_file, count in test_cases:
        print(f"{title} ({count} tests)")
        print(f"   {desc}\n")
    
    input(f"{bcolors.WARNING}[Presiona ENTER para ejecutar todos los tests]{bcolors.ENDC}")
    
    # Ejecutar todos los tests
    separator("EJECUTANDO TODOS LOS TESTS", "═")
    print(f"{bcolors.OKBLUE}$ pytest tests/ -v{bcolors.ENDC}\n")
    
    result = run_tests()
    print(result.stdout)
    
    # Parsear resultados
    lines = result.stdout.split('\n')
    summary_line = [l for l in lines if 'passed' in l.lower()]
    
    if result.returncode == 0:
        print(f"\n{bcolors.OKGREEN}{bcolors.BOLD}✅ TODOS LOS TESTS PASARON EXITOSAMENTE{bcolors.ENDC}\n")
    else:
        print(f"\n{bcolors.FAIL}{bcolors.BOLD}❌ ALGUNOS TESTS FALLARON{bcolors.ENDC}\n")
    
    # Resumen
    separator("RESUMEN DE RESULTADOS")
    
    passed = result.stdout.count(" PASSED")
    failed = result.stdout.count(" FAILED")
    
    print(f"{'='*70}")
    print(f"  ✅ Tests Pasados:    {passed:2}")
    print(f"  ❌ Tests Fallidos:   {failed:2}")
    print(f"  📊 Total:            {passed + failed:2}")
    print(f"{'='*70}\n")
    
    # Cobertura por categoría
    categories = [
        ("Análisis Léxico", "test_jwt_valid"),
        ("Análisis Sintáctico", "test_jwt_malformed"),
        ("Análisis Semántico", "test_jwt_valid"),
        ("Validación Temporal", "test_jwt_expired"),
        ("Verificación Criptográfica", "test_jwt_bad_signature"),
    ]
    
    print("Cobertura por Fase:")
    for category, pattern in categories:
        count = sum(1 for line in result.stdout.split('\n') 
                   if pattern in line and 'PASSED' in line)
        if count > 0:
            print(f"  ✅ {category:30} {count:2} tests")
    
    print()

def quick_mode():
    """Modo rápido - solo ejecutar y mostrar resultados"""
    separator("EJECUTANDO TESTS", "═")
    result = run_tests()
    print(result.stdout)
    return result.returncode == 0

def detailed_mode():
    """Modo detallado - test por test"""
    
    separator("MODO DETALLADO - TESTS POR CATEGORÍA")
    
    test_files = [
        ("✅ TOKENS VÁLIDOS", "test_jwt_valid.py"),
        ("⏰ TOKENS EXPIRADOS", "test_jwt_expired.py"),
        ("🔨 TOKENS MALFORMADOS", "test_jwt_malformed.py"),
        ("❌ FIRMA INVÁLIDA", "test_jwt_bad_signature.py"),
    ]
    
    results = []
    for emoji_name, test_file in test_files:
        separator(emoji_name, "─")
        print(f"{bcolors.OKBLUE}$ pytest tests/{test_file} -v{bcolors.ENDC}\n")
        
        result = run_tests(test_file)
        print(result.stdout)
        
        success = result.returncode == 0
        results.append((emoji_name, success))
        
        input(f"\n{bcolors.WARNING}[Presiona ENTER para continuar]{bcolors.ENDC}")
    
    # Resumen
    separator("RESUMEN FINAL")
    for title, success in results:
        status = f"{bcolors.OKGREEN}✅ PASS{bcolors.ENDC}" if success else f"{bcolors.FAIL}❌ FAIL{bcolors.ENDC}"
        print(f"{status}  {title}")

def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        print(f"\n{bcolors.BOLD}Modos disponibles:{bcolors.ENDC}")
        print("  python demo_tests.py demo     - Modo demostración interactivo")
        print("  python demo_tests.py quick    - Modo rápido")
        print("  python demo_tests.py detailed - Modo detallado (test por test)")
        print()
        mode = input("Selecciona un modo (demo/quick/detailed): ").lower()
    
    if mode == "demo":
        demo_mode()
    elif mode == "quick":
        quick_mode()
    elif mode == "detailed":
        detailed_mode()
    else:
        print(f"{bcolors.FAIL}Modo no reconocido{bcolors.ENDC}")
        sys.exit(1)
    
    print(f"\n{bcolors.OKGREEN}{bcolors.BOLD}¡Demostración completada!{bcolors.ENDC}\n")

if __name__ == "__main__":
    main()
