import boto3 
import json
import os

# Inicializa os clientes da AWS
s3 = boto3.client('s3')
textract = boto3.client('textract')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        print(f"\n🚀 INICIANDO PROCESSO TEXTRACT 🚀\n")
        print(f"📥 Evento recebido: {json.dumps(event, indent=4)}")  

        # 📌 Obtendo os parâmetros corretos
        file_name = event.get("file")
        bucket_name = event.get("bucket")

        if not file_name or not bucket_name:
            raise ValueError("❌ Parâmetros inválidos: 'file' e 'bucket' são obrigatórios!")

        print(f"📂 Arquivo recebido para processamento: s3://{bucket_name}/{file_name}")

        # 📝 Processa com Amazon Textract
        print("🔎 Extraindo informações do documento com Textract...")
        response = textract.analyze_document(
            Document={'S3Object': {'Bucket': bucket_name, 'Name': file_name}},  
            FeatureTypes=['TABLES', 'FORMS']
        )

        # 📄 Organiza os textos extraídos
        extracted_data = {"lines": [], "words": []}
        
        for block in response.get("Blocks", []):
            if block["BlockType"] == "LINE":
                extracted_data["lines"].append(block["Text"])
            elif block["BlockType"] == "WORD":
                extracted_data["words"].append(block["Text"])

        # 📂 Define o nome do arquivo de saída no S3
        output_key = file_name.replace("NFs/", "processado/").rsplit(".", 1)[0] + ".json"
        print(f"💾 Salvando JSON extraído em: s3://{bucket_name}/{output_key}")

        # 🚀 Salva o JSON no S3
        s3.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=json.dumps(extracted_data, indent=4),
            ContentType="application/json"
        )

        print("✅ Extração concluída e arquivo salvo no S3!")

        # 🔗 Chama a próxima Lambda (NLP com NLTK), se configurada
        next_lambda = os.environ.get('NEXT_LAMBDA_NLTK', '').strip()
        if next_lambda:
            try:
                print(f"🔄 Invocando Lambda NLP: {next_lambda}")
                lambda_client.invoke(
                    FunctionName=next_lambda,
                    InvocationType='Event',
                    Payload=json.dumps({'bucket': bucket_name, 'file': output_key})
                )
                print("✅ Lambda NLP invocada com sucesso!")
            except Exception as e:
                print(f"⚠️ Erro ao chamar Lambda {next_lambda}: {str(e)}")
        else:
            print("⚠️ NEXT_LAMBDA_NLTK não definido, pulando chamada.")

            print("🎉 PROCESSAMENTO FINALIZADO COM SUCESSO! 🎉")

# 🚀 Atualizando a saída da Lambda Textract
        return {
            'statusCode': 200,
            "bucket": bucket_name,
            "file": output_key  
          }

    except Exception as e:
        print(f"\n❌ ERRO FATAL: {str(e)}\n")
        return {'statusCode': 500, 'body': f'Erro ao processar arquivo: {str(e)}'} 