import json
from upload_invoice import lambda_handler as upload_invoice

# Dicionário de rotas da API
routes = {
    "POST /api/v1/invoice": upload_invoice
}
