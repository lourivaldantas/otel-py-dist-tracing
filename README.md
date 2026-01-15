# Client Server API Docker
> Sistema de duas APIs (Cliente/Servidor) integradas via Docker Network.

## Criar duas APIs
### 1. server-api:
- Expor a rota GET /users,
- Essa rota deve consumir a API externa: https://jsonplaceholder.typicode.com/users,
    
### 2. client-api:
- Expor a rota GET /getUsers
- Essa rota deve chamar a API server, que por sua vez chama a API externa,


## Objetivos
### Inicial
- Garantir propagação de contexto entre:
- client-api → server-api → API externa,

### Container Docker
- Configurar ambas as APIs com:
1. Dockerfile
2. docker-compose (opcional, mas desejável),

### Instrumentalização
- Instrumentar ambas as APIs com OpenTelemetry (SDK), gerando:
1. Traces
2.  Logs (em formato json),
3. Metrics,

### Outras configurações
- Configurar um OpenTelemetry Collector
- Receber telemetria via OTLP
- Processar dados (batch, memory limiter, etc.)

## Integrar a Coralogix
- Integrar a aplicação instrumentalizada a Coralogix.

### Modelo de .env
```
CORALOGIX_DOMAIN={seu domínio}
CORALOGIX_PRIVATE_{sua chave}
CORALOGIX_APP_NAME={nome da aplicação}
CORALOGIX_SUB_NAME={subnome da aplicação}
```
