import json
import requests
import os
import boto3

#refatorar fuunções depois

# Configuração da API Groq
GROQ_API_KEY = "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"  # Defina essa variável no ambiente
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


def verificar_forma_pgto(json_response):
    if json_response['forma_pgto'].lower() in ['dinheiro', 'pix']:
        return 'dinheiro/pix'
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


def call_groq_api():
    """Envia a nota fiscal para a API da Groq e retorna a resposta corrigida."""
    if not GROQ_API_KEY:
        raise ValueError("API Key da Groq não encontrada. Defina a variável de ambiente GROQ_API_KEY.")

    prompt = f"""Tente corrigir da melhor maneira possível a seguinte nota fiscal:
    Não substitua ou mexa em campos que já estão preenchidos.
    Caso o campo esteja vazio(null), substitua por "None"(com aspas para manter o formato json). 
    Retorne apenas a nota fiscal já corrigida sem mensagens extras, em formato JSON válido, use aspas duplas.

    
    "nome_emissor": "Pedro da Silva",
    "CNPJ_emissor": "00.000.000/0000-0a",
    "endereco_emissor": "",
    "CNPJ_CPF_consumidor": "000.000.0a0-00",
    "data_emissao": "00/00/0000",
    "numero_nota_fiscal": "",
    "serie_nota_fiscal": "",
    "valor_total": "0000.00",
    "forma_pgto": "<dinheiropix/outros>"
    
    """

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
    
        data = response.json()

        if "choices" not in data or not data["choices"]:
            raise ValueError("Resposta da API Groq inválida: 'choices' ausente ou vazio.")

        return json.loads(data["choices"][0]["message"]["content"])

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erro na requisição para a API Groq: {str(e)}")
    except json.JSONDecodeError:
        raise ValueError("Erro ao decodificar a resposta da API Groq. Resposta não é um JSON válido.")


def lambda_handler(event, context):
    """Função principal da Lambda para teste."""
    try:
        # JSON de teste passado na própria requisição
        #nota_fiscal = event.get("nota_fiscal")
        #if not nota_fiscal:
            #raise ValueError("Nenhuma nota fiscal fornecida no evento.")


        #print("Nota Fiscal Recebida:", json.dumps(nota_fiscal, indent=2))

        # Processa a nota fiscal com a API Groq
        nota_corrigida = call_groq_api()
        #json_response = nota_corrigida.get("choices", [{}])[0].get("message", {}).get("content", "")
        print("Tentativa content")
        json_response = parse_json(nota_corrigida)


        # Verificar a forma de pagamento
        forma_pgto = verificar_forma_pgto(json_response)
        #print(forma_pgto)

        print("Nota Fiscal Corrigida:", json_response)

        return {
            "status": "sucesso",
            "nota_corrigida": json_response,
            "forma_pgto": forma_pgto
        }
    except Exception as e:
        print(f"Erro: {str(e)}")
        return {
            "status": "erro",
            "detalhes": str(e)
        }
