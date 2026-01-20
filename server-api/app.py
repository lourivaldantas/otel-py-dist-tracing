import requests
from flask import Flask
from infra.telemetry import *
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Inicializa a stack de telemetria (metrics, traces e logs)
configure_opentelemetry()

# Instrumentaliza a biblioteca 'Requests' para o rastreio de chamadas HTTP externas
RequestsInstrumentor().instrument()

app = Flask(__name__)

# Instrumentalzia a biblioteca 'Flask' para a captura automática de requisições e spans
FlaskInstrumentor().instrument_app(app)

# obter tracer para a criação de spans manuais
tracer = trace.get_tracer(__name__)

@app.route("/users")
@tracer.start_as_current_span("serverApi")


def serverApi():
    logging.info("Buscando usuários...")
    
    # Consumo de API externa com propagação de conexão de contexto automática
    users = requests.get("https://jsonplaceholder.typicode.com/users").json()
    logging.info(f"Sucesso! {len(users)} usuários encontrados.")
    return users

if __name__ == "__main__":
    # Execução de serviço em modo debug (host 0.0.0.0 para acesso via Docker)
    app.run(host="0.0.0.0", port=5000, debug=True)
