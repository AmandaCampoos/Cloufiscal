import json
import re

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