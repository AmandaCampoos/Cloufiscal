<div align="justify">

# 📌 CLOUDFISCAL - Processamento de Notas Fiscais

<div align="center">
  <img src="assets/CloudFiscal.png" alt="CloudFiscal" width="200" height="200">
</div>

## Visão Geral
Este projeto é um sistema automatizado para processamento de notas fiscais, utilizando AWS Lambda, API Gateway, S3, Textract, NLTK e Step Functions para orquestração do fluxo de trabalho. O objetivo é extrair e estruturar informações das notas fiscais enviadas pelos usuários.


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
- AWS Step Functions -
- AWS CloudWatch - 

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

- Responsável por interagir com o CloudWatch e utilizar variáveis de ambiente.
- Define as rotas e invoca a API Gateway.
- Faz o upload da nota fiscal para o bucket S3 na pasta `NFS/`.
- Inicia o Step Function para orquestrar o fluxo de trabalho.

### Lambda 2 - `LambdaTextract`:

- Processa imagens das notas fiscais (PNG ou JPG, uma por vez).
- Utiliza o serviço Amazon Textract para ler o texto da imagem e extrair os dados estruturados.
- Processa as informações extraídas e as devolve no formato JSON.
- Ao final, chama a próxima função Lambda, `lambda_NLTK`, para continuar o processamento.

### Lambda 3 - `LambdaNLTK`:

- Utiliza a biblioteca NLTK (Natural Language Toolkit) para processamento de texto.
- Faz uso de Layers contendo as dependências do NLTK e configura o caminho para essas layers.
- A função lambda_handler acessa o bucket S3 de entrada (pasta "processado") e de saída (pasta "estruturados").
- Organiza e processa os dados extraídos pela função anterior, baixa o arquivo JSON do S3 e salva a versão estruturada no mesmo bucket.
- Retorna um status code indicando o sucesso ou falha do processo.

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
