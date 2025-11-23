#!/bin/bash
# Script para desplegar en AWS usando CloudShell (sin instalar nada)
# Copia y pega este contenido en AWS CloudShell

echo "🚀 Despliegue de JWT Analyzer en AWS Elastic Beanstalk"
echo "======================================================"

# Variables
APP_NAME="jwt-analyzer"
ENV_NAME="jwt-analyzer-prod"
REGION="us-east-1"
BUCKET_NAME="jwt-analyzer-$(date +%s)"

echo -e "\n📝 PASO 1: Crear bucket S3 para código"
aws s3 mb s3://$BUCKET_NAME --region $REGION

echo -e "\n📦 PASO 2: Preparar código para upload"
# Esto descargará y preparará el código
cd /tmp
git clone https://github.com/Juliana-2210/Analizador-jwt.git jwt-analyzer-repo
cd jwt-analyzer-repo

echo -e "\n📤 PASO 3: Subir código a S3"
zip -r code.zip . -x ".git/*" ".gitignore" "__pycache__/*" "*.pyc" ".env"
aws s3 cp code.zip s3://$BUCKET_NAME/

echo -e "\n✅ PASO 4: Crear aplicación Elastic Beanstalk"
aws elasticbeanstalk create-application \
    --application-name $APP_NAME \
    --region $REGION 2>/dev/null || echo "Aplicación ya existe"

echo -e "\n🔧 PASO 5: Crear versión de la aplicación"
aws elasticbeanstalk create-application-version \
    --application-name $APP_NAME \
    --version-label "v1-$(date +%s)" \
    --source-bundle "S3Bucket=$BUCKET_NAME,S3Key=code.zip" \
    --region $REGION

VERSION_LABEL=$(aws elasticbeanstalk describe-application-versions \
    --application-name $APP_NAME \
    --region $REGION \
    --query 'ApplicationVersions[0].VersionLabel' \
    --output text)

echo "Version creada: $VERSION_LABEL"

echo -e "\n🌍 PASO 6: Crear entorno"
aws elasticbeanstalk create-environment \
    --application-name $APP_NAME \
    --environment-name $ENV_NAME \
    --environment-tier Name=WebServer,Type=Standard \
    --instance-type t3.micro \
    --version-label $VERSION_LABEL \
    --region $REGION \
    --option-settings \
        Namespace=aws:autoscaling:launchconfiguration,OptionName=InstanceType,Value=t3.micro \
        Namespace=aws:ec2:instances,OptionName=InstanceTypes,Value=t3.micro \
    2>/dev/null || echo "Entorno ya existe"

echo -e "\n⏳ PASO 7: Esperar a que el entorno esté listo"
aws elasticbeanstalk wait environment-ready \
    --application-name $APP_NAME \
    --environment-name $ENV_NAME \
    --region $REGION

echo -e "\n📋 PASO 8: Configurar variables de entorno"
aws elasticbeanstalk update-environment \
    --application-name $APP_NAME \
    --environment-name $ENV_NAME \
    --option-settings \
        Namespace=aws:elasticbeanstalk:application:environment,OptionName=MONGODB_URI,Value="mongodb+srv://julianarincon01_db_user:qBicmS7UCQyUwhZw@jwt-analyzer-cluster.udetv8m.mongodb.net/jwt_analyzer?appName=jwt-analyzer-cluster" \
        Namespace=aws:elasticbeanstalk:application:environment,OptionName=FLASK_ENV,Value="production" \
    --region $REGION

echo -e "\n✅ PASO 9: Obtener URL del entorno"
ENDPOINT=$(aws elasticbeanstalk describe-environments \
    --application-name $APP_NAME \
    --environment-name $ENV_NAME \
    --region $REGION \
    --query 'Environments[0].CNAME' \
    --output text)

echo -e "\n🎉 ¡DESPLIEGUE COMPLETADO!"
echo "============================"
echo "✅ Aplicación: $APP_NAME"
echo "✅ Entorno: $ENV_NAME"
echo "✅ URL: http://$ENDPOINT"
echo "✅ Bucket S3: s3://$BUCKET_NAME"
echo -e "\nAccede a tu aplicación en: http://$ENDPOINT\n"

echo "📝 Para ver logs:"
echo "aws logs tail /aws/elasticbeanstalk/$APP_NAME/$ENV_NAME --follow"

echo "🛑 Para detener (CUIDADO - no se puede recuperar):"
echo "aws elasticbeanstalk terminate-environment --application-name $APP_NAME --environment-name $ENV_NAME"
