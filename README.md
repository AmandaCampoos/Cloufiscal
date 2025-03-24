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
3. [🔬 Testes locais](#-testes-locais)
4. [📦 Deployment](#-deployment)
5. [📝 Atribuições de Tarefas](#-atribuições-de-tarefas)  
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

### 💻 **Ferramentas de Desenvolvimento**

- Docker - Para execução local da Função Lambda
- Git e GitHub - Controle de versão
- Postman - Para testes locais

---

## 📝 Requisitos


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
      <a href="https://github.com/AmandaCampoos">Amanda Campos</a>
    </td>
    <td align="center">
      <img src="assets/BernardoA.png" alt="Bernardo Alonso" width="120" height="120" style="border-radius: 10px;">
      <br>
      <a href="https://github.com/Bernardo-rar">Bernardo Alonso</a>
    </td>
    <td align="center">
      <img src="assets/RobertaO.png" alt="Roberta Oliveira" width="120" height="120">
      <br>
      <a href="https://github.com/Bernardo-rar">Roberta Oliveira</a>
    </td>
  </tr>
</table>

 

</div>
