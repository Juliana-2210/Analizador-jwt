# Analizador JWT

Aplicación web para analizar, crear y validar tokens JWT.

## ¿Qué hace?

- Crea tokens JWT personalizados
- Analiza tokens existentes
- Verifica firmas
- Muestra cuándo expira un token
- Guarda tokens en base de datos MongoDB

## Cómo usar localmente

1. Instala dependencias:
```bash
pip install -r requirements.txt
```

2. Crea archivo `.env` con tu conexión a MongoDB:
```
MONGODB_URI=tu_conexion_mongodb
```

3. Ejecuta la aplicación:
```bash
python app.py
```

4. Abre en navegador: `http://localhost:5000`

## Despliegue en AWS

La aplicación está desplegada en AWS Elastic Beanstalk.

**URL de producción:** http://jwt-analyzer-prod.eba-sqdmfwrs.us-east-1.elasticbeanstalk.com

### Para redesplegar:

1. Abre AWS CloudShell
2. Ve al directorio del proyecto
3. Ejecuta: `eb deploy`

## Estructura del proyecto

```
├── app.py              # Aplicación principal Flask
├── jwt_analyzer/       # Módulos del analizador
├── templates/          # Interfaz web
├── static/            # CSS y archivos estáticos
├── tests/             # Tests unitarios
├── Procfile           # Configuración AWS
└── requirements.txt   # Dependencias Python
```

## Tecnologías

- Python 3.11
- Flask (web framework)
- MongoDB Atlas (base de datos)
- AWS Elastic Beanstalk (hosting)
- Gunicorn (servidor producción)

## Tests

Ejecutar tests:
```bash
pytest tests/
```
