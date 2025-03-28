<div align="justify">

# 🧾 CLOUDFISCAL - Processamento de Notas Fiscais

<div align="center">
  <img src="assets/CloudFiscal.png" alt="CloudFiscal" width="200" height="200">
</div>

## 📌 Visão Geral
Este projeto implementa um sistema automatizado para processamento de notas fiscais, utilizando serviços da AWS para extrair, processar e estruturar informações de forma eficiente. A arquitetura é baseada em AWS Lambda, API Gateway, S3, Textract, NLTK e Step Functions, garantindo escalabilidade e automação do fluxo de trabalho.

O principal objetivo é extrair, processar e organizar os dados das notas fiscais enviadas pelos usuários, transformando-os em um formato estruturado para facilitar análises.


![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AWS SAM](https://img.shields.io/badge/AWS%20SAM-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Amazon AWS API Gateway](https://img.shields.io/badge/AWS%20API%20Gateway-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Amazon AWS S3](https://img.shields.io/badge/AWS%20S3-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Amazon AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Amazon AWS Textract](https://img.shields.io/badge/AWS%20Textract-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Boto3](https://img.shields.io/badge/Boto3-4B8BBE?style=for-the-badge&logo=python&logoColor=white)
![LLM](https://img.shields.io/badge/LLM-Blue?style=for-the-badge)
![NLTK](https://img.shields.io/badge/NLTK-008000?style=for-the-badge&logo=python&logoColor=white)

---

## 📖 Índice

1. [🚀 Tecnologias Utilizadas](#-tecnologias-utilizadas)
2. [📝 Requisitos](#-requisitos) 
3. [🛠️ Arquitetura e Funcionalidades](#-arquitetura-e-funcionalidade)
3. [🔬 Testes locais](#-testes-locais)
4. [📦 Deployment](#-deployment)
5. [📝 Responsabilidades da equipe](#-responsabilidades-da-equipe)  
6. [👨‍💻 Autores](#-autores)
7. [📂 Estrutura de Pastas](#-estrutura-de-pastas)
8. [💻 Print da Página](#-print-da-pagina)

---

## 🚀 Tecnologias Utilizadas  

### 🐍 **Linguagem**

- Python 3.12  

### 🛠️ **Frameworks e Bibliotecas**

- AWS SAM - Serverless Application Model
- Boto3 - SDK da AWS para Python
- NLTK - Biblioteca para processamento de linguagem natural

### ☁️ **Serviços AWS**

- Lambda - Execução de código serverless  
- API Gateway - Exposição de endpoints
- Bucket S3 - Armazenamento do arquivos  
- Textract - Extração de dados de notas fiscais
- AWS Step Functions - Orquestração do fluxo de processamento
- AWS CloudWatch - Monitoramento e logs

### 💻 **Ferramentas de Desenvolvimento**

- Docker - Para execução local da Função Lambda
- Git e GitHub - Controle de versão
- Postman - Para testes locais

---

## 📝 Requisitos
Para executar o projeto localmente, você precisará:

- Python 3.12 instalado

- AWS CLI configurado

- AWS SAM instalado

- Docker instalado para testes locais das Lambdas

- Postman ou outra ferramenta para testar os endpoints

- Conta AWS com permissões para Lambda, S3, API Gateway e Textract

## 🛠️ Arquitetura e Funcionalidades

### 🔄 Fluxo de Processamento

###  Lambda 1 - `InvoiceFunction`:

##### Responsável por iniciar o fluxo de processamento e interagir com os serviços AWS:

- Monitora eventos do CloudWatch e utiliza variáveis de ambiente para configuração.

- Define as rotas da API e interage com o API Gateway.

- Faz o upload da nota fiscal para o bucket S3, armazenando-a na pasta `NFs/`.

- Inicia o Step Function, que gerencia a execução das próximas etapas do processo.

### Lambda 2 - `LambdaTextract`:

##### Processa a nota fiscal utilizando OCR via Amazon Textract:

- Acessa a nota fiscal armazenada no S3 na pasta `NFs/`.

- Suporta múltiplos formatos de imagem para extração de dados.

- Utiliza o Amazon Textract para converter o conteúdo da nota fiscal em texto, palavra por palavra.

- Salva o resultado em JSON na pasta `processado/` do S3.

- Ao concluir, aciona a próxima função `LambdaNLTK` para estruturar os dados extraídos.

### Lambda 3 - `LambdaNLTK`:

##### Aplica processamento de linguagem natural (NLP) para estruturar os dados extraídos:

- Utiliza NLTK (Natural Language Toolkit) e Regex para refinar o texto.

- Emprega AWS Lambda Layers para carregar as dependências do NLTK.

- Acessa os buckets S3:

  - Lê o JSON processado na pasta `processado/`.

  - Estrutura os dados extraídos pela função anterior e salva na pasta `estruturado/`.

- Retorna um status code indicando sucesso ou falha do processamento.


### Lambda 4 - `LambdaLLM`:
- 
 -

## 🔬 Testes Locais

1. **Usando Postman**:

   - Faça um POST para `/api/v1/invoice` enviando um arquivo como `multipart/form-data`.

2. **Usando AWS SAM**:

   - Rodar `sam local invoke` para testar funções Lambda individualmente.
   - Rodar `sam local start-api` para testar a API Gateway localmente.

---


## 📦 Deployment

Para implantar a aplicação na AWS:

```sh
sam build
saM deploy --guided --profile Nome-de-Usuário

```

## 📝 Responsabilidades da equipe:

- Roberta: Desenvolvimento da API REST e integração com o S3 utilizando AWS SAM.

- Amanda: Implementação do Textract e uso do NLTK para processamento de dados.

- Bernardo: Desenvolvimento e integração do modelo de LLM (Large Language Model).

## 💻 Print da Página

<div align="center">
  <img src="./assets/PrintPagina.png" alt="Pagina" width="650">
</div>


## 📂 Estruturas de pastas

```plaintext
sprints-4-5-6-pb-aws-janeiro/
│── .aws-sam/
│   ├── build/
│   ├── cache/
│   ├── artifacts/
│── assets/
│   ├── images/
│   ├── docs/
│── dataset/
│   ├── raw_data/
│   ├── processed_data/
│   ├── NFs.zip
│── lambda_api_gateway/
│   ├── upload_nf/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   ├── styles.css
│   │   │   ├── js/
│   │   │   │   ├── script.js
│   │   ├── templates/
│   │   │   ├── index.html
│   │   ├── app.py
│   │   ├── routes.py
│   ├── upload_invoice/
│   │   ├── handlers/
│   │   ├── utils/
│   │   ├── upload_invoice.py
│── lambda_llm/
│   ├── models/
│   ├── utils/
│   ├── app.py
│   ├── requirements.txt
│── lambda_nltk/
│   ├── processors/
│   ├── utils/
│   ├── app.py
│   ├── requirements.txt
│── lambda_textract/
│   ├── parsers/
│   ├── utils/
│   ├── app.py
│   ├── requirements.txt
│── layer/
│   ├── nltk/
│   │   ├── NLTK_layer.zip
│── statemachine/
│   ├── definitions/
│   │   ├── invoice_processor.json
│── .gitignore
│── README.md
│── requirements.txt
│── samconfig.toml
|── template.yaml

```
 
## 🤝 Autores  

<table>
  <tr>
    <td align="center">
      <img src="assets/AmandaX.png" alt="Amanda Campos" width="120" height="120">
      <br>
      <a href="https://github.com/AmandaCampoos">Git Hub - Amanda Campos</a>
      <br>
      <a href="linkedin.com/in/amanda-ximenes-a02ab8266">Linkedin - Amanda Campos</a>
    </td>
    <td align="center">
      <img src="assets/BernardoA.png" alt="Bernardo Alonso" width="120" height="120">
      <br>
      <a href="https://github.com/Bernardo-rar"> Git Hub - Bernardo Alonso</a>
      <br>
      <a href="https://github.com/Bernardo-rar"> Linkedin - Bernardo Alonso</a>
    </td>
    <td align="center">
      <img src="assets/RobertaO.png" alt="Roberta Oliveira" width="120" height="120">
      <br>
      <a href="https://github.com/RobertakOliveira">Git Hub - Roberta Oliveira</a>
      <br>
      <a href="linkedin.com/in/roberta-oliveira-b9a0961a4">Linkedin - Roberta Oliveira</a>
    </td>
  </tr>
</table>


 

</div>
