import boto3
import json
import os

# Inicializa os clientes da AWS
s3 = boto3.client('s3')
textract = boto3.client('textract')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        # 🔍 Obtém informações do evento do S3
        record = event['Records'][0]
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']

        print(f"📥 Recebendo arquivo: s3://{s3_bucket}/{s3_key}")

        # 📝 Processa com Amazon Textract
        response = textract.analyze_document(
            Document={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},  
            FeatureTypes=['TABLES', 'FORMS']
        )

        # 📄 Extrai e formata a resposta como JSON
        extracted_text = json.dumps(response, indent=4)

        # 📂 Define o nome do arquivo de saída no S3
        output_key = s3_key.replace("NFs/", "processado/").rsplit(".", 1)[0] + ".json"

        print(f"💾 Salvando JSON extraído em: s3://{s3_bucket}/{output_key}")

        # 🚀 Salva o JSON no S3
        s3.put_object(
            Bucket=s3_bucket,
            Key=output_key,
            Body=extracted_text,
            ContentType="application/json"
        )

        # 🔗 Chama a próxima Lambda (NLP com NLTK), se configurada
        next_lambda = os.environ.get('NEXT_LAMBDA_NLTK', '').strip()
        if next_lambda:
            try:
                print(f"🔄 Invocando Lambda NLP: {next_lambda}")
                lambda_client.invoke(
                    FunctionName=next_lambda,
                    InvocationType='Event',
                    Payload=json.dumps({'s3_bucket': s3_bucket, 's3_key': output_key})
                )
            except Exception as e:
                print(f"⚠️ Erro ao chamar Lambda {next_lambda}: {str(e)}")
        else:
            print("⚠️ NEXT_LAMBDA_NLTK não definido, pulando chamada.")

        return {'statusCode': 200, 'body': f'Textract processado e salvo em {output_key}'}

    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return {'statusCode': 500, 'body': f'Erro ao processar arquivo: {str(e)}'}
