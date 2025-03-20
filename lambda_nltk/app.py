import os
import json
import boto3
import nltk
print("NLTK Data Path:", nltk.data.path)
from nltk.tokenize import word_tokenize

# Configurar o caminho da Layer
nltk.data.path.append("/opt/python/nltk_data")

s3_client = boto3.client("s3")

def lambda_handler(event, context):
    bucket_name = "minhas-notas-fiscais"
    input_prefix = "processado/"
    output_prefix = "estruturados/"

    # Verifica se o evento tem a chave "Records" (caso venha do S3)
    if "Records" in event:
        records = event["Records"]
        input_key = records[0]["s3"]["object"]["key"]
    # Verifica se veio um evento direto do Step Functions
    elif "s3_key" in event:
        input_key = event["s3_key"]
    else:
        return {
            "statusCode": 400,
            "error": "Evento mal formatado. Nenhuma chave 'Records' ou 's3_key' encontrada."
        }

    # Verifica se o arquivo está no caminho correto
    if not input_key.startswith(input_prefix):
        return {
            "statusCode": 400,
            "error": f"O arquivo {input_key} não está no diretório esperado."
        }

    output_key = input_key.replace(input_prefix, output_prefix).replace(".json", "-structured.json")

    try:
        # Baixar o arquivo JSON do S3
        obj = s3_client.get_object(Bucket=bucket_name, Key=input_key)
        text_data = json.loads(obj["Body"].read().decode("utf-8"))

        # Tokenizar o texto
        structured_data = {
            "invoice_id": input_key.split("/")[-1].replace(".json", ""),
            "tokens": word_tokenize(text_data.get("raw_text", ""))
        }

        # Salvar JSON estruturado no S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=json.dumps(structured_data, indent=4),
            ContentType="application/json"
        )

        return {
            "statusCode": 200,
            "message": f"Arquivo processado e salvo em {output_key}"
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "error": f"Erro ao processar o arquivo: {str(e)}"
        }
