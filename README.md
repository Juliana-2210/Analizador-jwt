# JWT Analyzer - Proyecto Final LF

## Instalación
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Ejecutar tests
pytest -q

## Uso CLI
Crear un token:
python -m jwt_analyzer.cli create --payload '{"sub":"1","iat":1630000000,"exp":1630003600}' --secret mysecret

Validar:
python -m jwt_analyzer.cli validate <token> --secret mysecret

Decodificar:
python -m jwt_analyzer.cli decode <token>
