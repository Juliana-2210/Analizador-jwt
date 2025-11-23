#!/usr/bin/env python3
"""
Script simple para mostrar todos los tests de forma clara
Ejecuta: python run_all_tests.py
"""

import subprocess
import sys

def main():
    print("\n" + "="*80)
    print("  🧪 SUITE DE TESTS - ANALIZADOR Y VALIDADOR DE JWT")
    print("="*80)
    print()
    
    # Ejecutar pytest
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        text=True
    )
    
    # Mostrar resultado
    print("\n" + "="*80)
    if result.returncode == 0:
        print("  ✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
    else:
        print("  ❌ ALGUNOS TESTS FALLARON")
    print("="*80 + "\n")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
