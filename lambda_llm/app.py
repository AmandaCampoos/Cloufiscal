import json
import requests
import os
import boto3
import re

#refatorar fuunções depois

# Configuração da API Groq
GROQ_API_KEY = ""  # Defina essa variável no ambiente
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


def treat_name(archive_name):
    match = re.search(r'/(.*?)-', archive_name)
    if match:
        return match.group(1)
    return "FunçãoNPegou"

def verificar_forma_pgto(json_response):
    if json_response['forma_pgto'].lower() in ['dinheiro', 'pix']:
        return 'dinheiro'
    else:
        return 'outros'

def parse_json(content):

    if content:
        content = content.get("choices", [{}])[0].get("message", {}).get("content", {})

        # Verificando se o conteúdo é uma string JSON válida e transformando-a em um dicionário

        # Remover a palavra 'json' e os backticks
        content = content.replace("json", "").strip('`').strip()
        content = content.strip()
        try:
            # Transformando a string JSON em um dicionário
            return json.loads(content)
        except json.JSONDecodeError:
            print("Erro ao decodificar o JSON. Retornando um dicionário vazio.")
            return {}  # Se não for possível decodificar, retorna um dict vazio
    return {}


def call_groq_api(nota_fiscal):
    """Envia a nota fiscal para a API da Groq e retorna a resposta corrigida."""
    if not GROQ_API_KEY:
        raise ValueError("API Key da Groq não encontrada. Defina a variável de ambiente GROQ_API_KEY.")

    prompt = f"""Tente corrigir da melhor maneira possível a seguinte nota fiscal:
    Não substitua ou mexa em campos que já estão preenchidos.
    Caso o campo esteja vazio(null), substitua por "None"(com aspas para manter o formato json). 
    Retorne apenas a nota fiscal já corrigida sem mensagens extras, em formato JSON válido, use aspas duplas.

    
    """ + nota_fiscal

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Levanta um erro se o status for diferente de 200
        print("Status Code:", response.status_code)
        print("Headers:", response.headers)

        return response.json()  # Mostra a resposta completa como string
    

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erro na requisição para a API Groq: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError("Erro ao decodificar a resposta da API Groq. Resposta não é um JSON válido.")


def lambda_handler(event, context):
    """Função principal da Lambda para teste."""
    try:

        # Se o JSON tiver a chave "data", usa ela; senão, assume que o próprio JSON já é a nota fiscal.
        # Util para fins de testes locais
        print("📄 Começando o processamento da Lambda ")
        structured_data = event.get("data", event) 
        archive_name = event.get("message", event)

        print("✅ Dados do arquivo recuperados com sucesso")

        json_name = json.dumps(archive_name, indent=2)

        
        treated_name= treat_name(json_name) 

        print("📄 Tratando e recuperando o nome do arquivo:", treated_name)

        #structured_data = event.get("data", {})  # Dados estruturados da nota fiscal
        #structured_data = event
        
        json_dados = json.dumps(structured_data, indent=2)

        if structured_data:
            print("Dados estruturados recebidos:", structured_data)
        else:
            return {
                "statuscode": "400",
                "detalhes": "Nenhum dado estruturado recebido."
            }
    

        # Processa a nota fiscal com a API Groq
        print("📥 Enviando a nota fiscal para a API Groq ")
        nota_corrigida = call_groq_api(json_dados)
        
        print("✅ Nota fiscal corrigida com sucesso:", nota_corrigida)

        json_response = parse_json(nota_corrigida)

        print("✅ JSON tranformado com sucesso:", json_response)

        print("Verificando a forma de pagamento")
        # Verificar a forma de pagamento
        forma_pgto = verificar_forma_pgto(json_response)
        #print(forma_pgto)
        print("📥 Começando processamento do S3")
        s3_client = boto3.client("s3")
        bucket_name = "minhas-notas-fiscaiss"
        input_prefix = "estruturados/"
        output_prefix = "finalizados/"

        forma_pgto = verificar_forma_pgto(json_response)
        pasta = f"finalizados/{forma_pgto}"
        

        # Criando o caminho dinâmico
        output_key = f"{pasta}/{treated_name}"


        s3_client.put_object(
            Bucket=bucket_name,
            Key=output_key,
            Body=json.dumps(json_response, indent=4),
            ContentType="application/json"
        )


        print("✅ Processaamento finalizado com sucesso!")

        return {
            "statuscode": "200",
            "nota_corrigida": json_response,
            "forma_pgto": forma_pgto
        }
    except Exception as e:
        print(f"⚠️ Erro: {str(e)}")
        return {
            "statuscode": "400",
            "detalhes": str(e)
        }
