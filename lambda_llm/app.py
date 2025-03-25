import json
import requests
import os
import boto3

# Configuração da API Groq
GROQ_API_KEY = ""
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


def call_groq_api():
    """Envia a nota fiscal para a API da Groq e retorna a resposta corrigida."""
    if not GROQ_API_KEY:
        raise ValueError("API Key da Groq não encontrada. Defina a variável de ambiente GROQ_API_KEY.")

    prompt = f"""Tente completar da melhor maneira possível a seguinte nota fiscal:
    Caso o campo esteja vazio(null), substitua por None. 
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

        return response.text  # Mostra a resposta completa como string
    
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

        print("Nota Fiscal Corrigida:", nota_corrigida)

        return {
            "status": "sucesso",
            "nota_corrigida": nota_corrigida
        }
    except Exception as e:
        print(f"Erro: {str(e)}")
        return {
            "status": "erro",
            "detalhes": str(e)
        }
