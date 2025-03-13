import boto3
import json
import base64
import logging
import os
import cgi  # type: ignore # Biblioteca para lidar com multipart/form-data
from io import BytesIO

# Configuração do Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nome do Bucket S3 (vem da variável de ambiente)
BUCKET_NAME = os.environ['BUCKET_NAME']
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Log do evento recebido para depuração
        logger.info(f"Evento recebido: {json.dumps(event)}")

        # Verifica se o corpo da requisição existe
        if 'body' not in event or not event['body']:
            return {
                'statusCode': 400,
                'body': json.dumps({"message": "Corpo da requisição está vazio!"})
            }

        # Verifica o Content-Type
        content_type = event.get('headers', {}).get('Content-Type', '')
        if 'multipart/form-data' in content_type:
            # Trata multipart/form-data para upload de arquivos
            logger.info("Processando upload via multipart/form-data")

            # Decodifica o corpo da requisição
            body = base64.b64decode(event['body'])
            environ = {'REQUEST_METHOD': 'POST'}
            fp = BytesIO(body)

            # Lida com multipart/form-data
            headers = {'content-type': content_type}
            fs = cgi.FieldStorage(fp=fp, environ=environ, headers=headers)

            if 'file' not in fs or not fs['file'].filename:
                return {
                    'statusCode': 400,
                    'body': json.dumps({"message": "Arquivo não encontrado na requisição!"})
                }

            # Extrai o arquivo e o nome
            file_item = fs['file']
            file_name = file_item.filename
            file_content = file_item.file.read()

            # Faz upload do arquivo para o S3
            s3_client.put_object(Bucket=BUCKET_NAME, Key=f'NFs/{file_name}', Body=file_content)

            return {
                'statusCode': 200,
                'body': json.dumps({"message": "Upload realizado com sucesso!"})
            }

        # Se não for multipart/form-data, retorna erro
        return {
            'statusCode': 415,
            'body': json.dumps({"message": "Content-Type não suportado!"})
        }

    except Exception as e:
        logger.error(f"Erro durante o upload: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({"message": "Erro interno no servidor"})
        }