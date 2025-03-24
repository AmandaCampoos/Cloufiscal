import json
import routes
from upload_invoice import lambda_handler as upload_invoice

# funçãoo
def lambda_handler(event, context):
    """Gerencia as requisições HTTP e direciona para as rotas corretas."""
    method = event.get("httpMethod", "")
    path = event.get("path", "")
    route_key = f"{method} {path}"

    handler = routes.routes.get(route_key, None)
    
    if handler:
        return handler(event, context)
    else:
        return {"statusCode": 404, "body": json.dumps({"erro": "Rota não encontrada"})}
