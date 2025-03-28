import os 
import json
import re
import boto3
import nltk

# Configurar o caminho da Layer NLTK na AWS Lambda
nltk.data.path.append("/opt/python/nltk_data")

# Inicializa o cliente S3
s3_client = boto3.client("s3")

# Padrões de regex para extração de dados
REGEX_PATTERNS = {
    "CNPJ": r"\d{14}|\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}",
    "CPF": r"\d{11}|\d{3}\.\d{3}\.\d{3}-\d{2}",
    "DATA": r"\d{2}/\d{2}/\d{4}",
    "VALOR": r"\d{1,3}(?:\.\d{3})*,\d{2}|\d+\.\d{2}",
    "NUMERO_NF": r"\b\d{6,}\b",
    "FORMA_PGTO": r"\b(Pix|Dinheiro|Cartão|Boleto|Crédito|Débito)\b"
}

def log(message):
    print(f"📝 {message}")

def extract_field(pattern, text, default="None"):
    """Extrai um campo usando regex e retorna o primeiro valor encontrado ou 'None'. """
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else default

def lambda_handler(event, context):
    log("Iniciando processamento da nota fiscal... 📄")
    
    bucket_name = "minhas-notas-fiscais-api-a"
    input_prefix = "processado/"
    output_prefix = "estruturado/"
    
    input_key = event.get("file")  
    
    if not input_key:
        log("⚠️ Nenhum arquivo encontrado no evento!")
        return {"statusCode": 400, "error": "Nenhum arquivo foi encontrado no evento."}
    
    log(f"📂 Arquivo recebido: {input_key}")
    
    if "processado/" not in input_key:
        log(f"❌ Arquivo está no local errado: {input_key}")
        return {"statusCode": 400, "error": f"Arquivo processado não encontrado! Esperado em '{input_prefix}', mas veio '{input_key}'."}
    
    output_key = input_key.replace(input_prefix, output_prefix).replace(".json", "-structured.json")
    
    try:
        log("📥 Baixando arquivo do S3...")
        obj = s3_client.get_object(Bucket=bucket_name, Key=input_key)
        text_data = json.loads(obj["Body"].read().decode("utf-8"))
        
        lines = text_data.get("lines", [])
        raw_text = " ".join(lines)
        
        log("🔍 Extraindo informações da nota fiscal...")
        structured_data = {
            "nome_emissor": extract_field(r"([\w\s]+) LTDA", raw_text),
            "CNPJ_emissor": extract_field(REGEX_PATTERNS["CNPJ"], raw_text),
            "endereco_emissor": extract_field(r"End.:([\w\s,.-]+)", raw_text),
            "CNPJ_CPF_consumidor": extract_field(REGEX_PATTERNS["CPF"], raw_text),
            "data_emissao": extract_field(REGEX_PATTERNS["DATA"], raw_text),
            "numero_nota_fiscal": extract_field(REGEX_PATTERNS["NUMERO_NF"], raw_text),
            "serie_nota_fiscal": extract_field(r"SAT No. (\d+)", raw_text),
            "valor_total": extract_field(REGEX_PATTERNS["VALOR"], raw_text),
            "forma_pgto": extract_field(REGEX_PATTERNS["FORMA_PGTO"], raw_text, "Outros")
        }
        
        log("📤 Salvando JSON estruturado no S3...")
        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=json.dumps(structured_data, indent=4),
            ContentType="application/json"
        )
        
        log("✅ Processamento concluído com sucesso!")
        return {
            "statusCode": 200,
            "message": f"Arquivo processado e salvo em {output_key}",
            "data": structured_data
        }
    
    except Exception as e:
        log(f"❌ Erro ao processar o arquivo: {str(e)}")
        return {
            "statusCode": 500,
            "error": f"Erro ao processar o arquivo: {str(e)}"
        }
