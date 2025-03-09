import boto3
import json
import logging

# Configuração do Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    """Função temporária apenas para teste da API"""
    return {
        'statusCode': 200,
        'body': json.dumps({"message": "Lambda ativa, mas upload desativado no momento."})
    }
