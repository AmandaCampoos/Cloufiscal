import json
import requests
import os

def call_groq_api(nota_fiscal):
    GROQ_API_KEY = ""  # Defina essa variável no ambiente
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "llama-3.3-70b-versatile"

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