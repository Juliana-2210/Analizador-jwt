# Script PowerShell para configurar AWS y desplegar en Elastic Beanstalk
# Ejecuta este script en PowerShell (como administrador)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "🚀 DESPLIEGUE DE JWT ANALYZER EN AWS" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan

# PASO 1: Verificar/Instalar AWS CLI
Write-Host "`n▶ PASO 1: Verificar AWS CLI..." -ForegroundColor Yellow

$awsCheck = aws --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ AWS CLI instalado: $awsCheck" -ForegroundColor Green
} else {
    Write-Host "⚠️  AWS CLI no instalado. Descargando..." -ForegroundColor Yellow
    
    # Descargar y ejecutar instalador
    $msiUrl = "https://awscli.amazonaws.com/AWSCLIV2.msi"
    $msiPath = "$env:TEMP\AWSCLIV2.msi"
    
    Write-Host "   Descargando desde: $msiUrl"
    (New-Object Net.WebClient).DownloadFile($msiUrl, $msiPath)
    
    Write-Host "   Ejecutando instalador..."
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i $msiPath /qn" -Wait
    
    Write-Host "✅ AWS CLI instalado" -ForegroundColor Green
    
    # Actualizar PATH
    $env:Path += ";C:\Program Files\Amazon\AWSCLIV2"
}

# PASO 2: Verificar EB CLI
Write-Host "`n▶ PASO 2: Verificar Elastic Beanstalk CLI..." -ForegroundColor Yellow

$ebCheck = eb --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ EB CLI instalado: $ebCheck" -ForegroundColor Green
} else {
    Write-Host "⚠️  Instalando EB CLI..." -ForegroundColor Yellow
    pip install awsebcli
    Write-Host "✅ EB CLI instalado" -ForegroundColor Green
}

# PASO 3: Configurar credenciales
Write-Host "`n▶ PASO 3: Configurar credenciales de AWS..." -ForegroundColor Yellow

# Leer del .env
$envFile = ".\.env"
$env:AWS_ACCESS_KEY_ID ="
$env:AWS_SECRET_ACCESS_KEY =
$env:AWS_DEFAULT_REGION = "us-east-1"

# Configurar AWS CLI
aws configure set aws_access_key_id $env:AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $env:AWS_SECRET_ACCESS_KEY
aws configure set default.region $env:AWS_DEFAULT_REGION

Write-Host "✅ Credenciales configuradas" -ForegroundColor Green

# PASO 4: Probar conexión
Write-Host "`n▶ PASO 4: Probar conexión a AWS..." -ForegroundColor Yellow

$caller = aws sts get-caller-identity 2>$null | ConvertFrom-Json

if ($caller) {
    Write-Host "✅ Conexión exitosa" -ForegroundColor Green
    Write-Host "   Account: $($caller.Account)"
    Write-Host "   UserId: $($caller.UserId)"
} else {
    Write-Host "❌ No se pudo conectar a AWS" -ForegroundColor Red
    Write-Host "   Verifica tus credenciales" -ForegroundColor Red
    exit 1
}

# PASO 5: Inicializar Elastic Beanstalk
Write-Host "`n▶ PASO 5: Inicializar Elastic Beanstalk..." -ForegroundColor Yellow

$appName = "jwt-analyzer"

# Verificar si ya está inicializado
$ebList = eb list 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ EB ya inicializado" -ForegroundColor Green
} else {
    Write-Host "   Inicializando aplicación: $appName"
    eb init -p "Python 3.11 running on 64bit Amazon Linux 2" $appName --region us-east-1
    Write-Host "✅ Inicialización completada" -ForegroundColor Green
}

# PASO 6: Crear o usar entorno
Write-Host "`n▶ PASO 6: Crear/Usar entorno..." -ForegroundColor Yellow

$envName = "jwt-analyzer-prod"
$mongoUri = "mongodb+srv://julianarincon01_db_user:qBicmS7UCQyUwhZw@jwt-analyzer-cluster.udetv8m.mongodb.net/jwt_analyzer?appName=jwt-analyzer-cluster"

# Verificar si el entorno ya existe
$envList = eb list | Select-String $envName
if ($envList) {
    Write-Host "✅ Entorno ya existe: $envName" -ForegroundColor Green
} else {
    Write-Host "   Creando entorno: $envName (puede tomar 5-10 minutos)"
    eb create $envName --instance-type t3.micro `
        --envvars MONGODB_URI="$mongoUri",FLASK_ENV=production
    Write-Host "✅ Entorno creado" -ForegroundColor Green
}

# PASO 7: Desplegar
Write-Host "`n▶ PASO 7: Desplegar aplicación..." -ForegroundColor Yellow

Write-Host "   Desplegando código..."
eb deploy
Write-Host "✅ Despliegue completado" -ForegroundColor Green

# PASO 8: Mostrar información
Write-Host "`n▶ PASO 8: Información del despliegue..." -ForegroundColor Yellow

Write-Host "`n📊 Estado del entorno:" -ForegroundColor Cyan
eb status

Write-Host "`n📱 URL de la aplicación:" -ForegroundColor Cyan
$url = eb open --print-url
Write-Host "✅ $url" -ForegroundColor Green

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "✅ ¡DESPLIEGUE COMPLETADO!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan

Write-Host "`n📝 Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Abre: eb open"
Write-Host "2. Verifica los logs: eb logs --stream"
Write-Host "3. Configura variables: eb setenv VARIABLE=valor"
Write-Host "4. Para detener: eb terminate $envName"

Write-Host "`n⏳ El despliegue puede tardar 2-3 minutos en activarse completamente." -ForegroundColor Cyan
Write-Host "🔗 Accede a: $url" -ForegroundColor Green
Write-Host "`n"
