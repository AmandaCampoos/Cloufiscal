import boto3
import json
import base64
import logging
import os
import cgi  # Biblioteca para lidar com multipart/form-dataa
from io import BytesIO

# Configuração do Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nome do Bucket S3 (vem da variável de ambiente)
BUCKET_NAME = os.environ['BUCKET_NAME']
STEP_FUNCTION_ARN = os.environ['STEP_FUNCTION_ARN']  # ARN da Step Function via variável de ambiente

# Clientes AWS
s3_client = boto3.client('s3')
stepfunctions_client = boto3.client('stepfunctions')

def lambda_handler(event, context):
    try:
        logger.info(f"Evento recebido: {json.dumps(event)}")

        if 'body' not in event or not event['body']:
            return {
                'statusCode': 400,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                'body': json.dumps({"message": "Corpo da requisição está vazio!"})

            }

        content_type = event.get('headers', {}).get('content-type', '')
        if 'multipart/form-data' in content_type:
            logger.info("Processando upload via multipart/form-data")

            # Decodifica o corpo da requisição
            body = base64.b64decode(event['body'])
            environ = {'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': content_type}
            fp = BytesIO(body)

            # Lida com multipart/form-data
            headers = {'content-type': content_type}
            fs = cgi.FieldStorage(fp=fp, environ=environ, headers=headers)

            if 'file' not in fs or not fs['file'].filename:
                return {
                    'statusCode': 400,
                    'headers': {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "POST, OPTIONS",
                        "Access-Control-Allow-Headers": "Content-Type"
                    },
                    'body': json.dumps({"message": "Arquivo não encontrado na requisição!"})
                }

            # Extrai o arquivo e o nome
            file_item = fs['file']
            file_name = file_item.filename
            file_content = file_item.file.read()
            s3_key = f'NFs/{file_name}'

            # Faz upload do arquivo para o S3
            s3_client.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=file_content)

            # Inicia a Step Function passando o caminho do arquivo
            response = stepfunctions_client.start_execution(
                stateMachineArn=STEP_FUNCTION_ARN,
                input=json.dumps({"s3_key": s3_key, "s3_bucket": BUCKET_NAME})
            )

            return {
                    'statusCode': 200,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "POST, OPTIONS",
                        "Access-Control-Allow-Headers": "Content-Type"
                },
                    'body': json.dumps({"message": "Upload realizado com sucesso e Step Function iniciada!"})
            }

        return {
            'statusCode': 415,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            'body': json.dumps({"message": "Content-Type não suportado!"})
        }

    except Exception as e:
        logger.error(f"Erro durante o upload: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            'body': json.dumps({"message": "Erro interno no servidor", "error": str(e)})
        }
