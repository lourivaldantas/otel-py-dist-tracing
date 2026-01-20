# 🌐 Client-Server API: Observability with OpenTelemetry & Coralogix

> Este projeto demonstra a implementação de um ecossistema de microserviços (Cliente/Servidor) focado em Observabilidade Full-stack. O objetivo principal é validar a propagação de contexto, coleta de telemetria distribuída e integração com a Coralogix utilizando o OpenTelemetry SDK.

## 🏗️ Arquitetura do Sistema

O fluxo de dados segue o seguinte percurso para garantir o rastreamento ponta a ponta:
1. **Client-API:** Recebe a requisição inicial e inicia o Root Span.
2. **Server-API:** Recebe a chamada via Docker Network, mantendo a continuidade do trace.
3. **External API:** Consumo de dados via JSONPlaceholder.
4. **OTel Collector:** Centraliza, processa e exporta os dados (Traces, Logs e Metrics) para a Coralogix via OTLP.

## 🛠️ Tecnologias e Ferramentas
- **Linguagem:** Python 3.x (Flask)
- **Instrumentação:** OpenTelemetry SDK (Python)
- **Containerização:** Docker & Docker Compose
- **Observabilidade:**
    - ***Traces:*** Rastreamento distribuído entre serviços.
    - ***Logs:*** Estruturados em formato JSON para melhor processamento.
    - ***Metrics:*** Monitoramento de performance e saúde das APIs.
- **Backend:** Coralogix via protocolo OTLP.

## 🚀 Como Executar
### 1. Configuração de Ambiente
O projeto utiliza variáveis de ambiente para gerenciar credenciais. Crie o arquivo .env baseado no exemplo:
```bash
cp .env.example .env
```
Preencha as variáveis com seus dados da Coralogix:

`CORALOGIX_PRIVATE_KEY`

`CORALOGIX_DOMAIN`

`APPLICATION_NAME`

`SUBSYSTEM_NAME`
### 2. Subir os Containers
```bash
docker-compose up -d --build
```

## 📊 Endpoints Disponíveis

| Serviço | Rota | Descrição |
| :---: | :---: | :---: |
| Client API | GET /getUsers | Inicia o fluxo chamando a Server API. |
| Server API | GET /users | Consome a API externa e retorna a lista de usuários. |

## 🔍 Detalhes da Instrumentação

### OpenTelemetry Collector
Configurado para atuar como gateway, processando dados em lote (batch) e limitando o uso de memória (memory_limiter) antes de exportar para o endpoint OTLP da Coralogix.

## 📈 Integração Coralogix
Ao rodar o projeto, os seguintes recursos ficam disponíveis:
- **Service Map:** Visualização automática das dependências.
- **Distributed Tracing:** Análise de latência entre o cliente e o servidor.
- **Custom Dashboards:** Gráficos baseados nas métricas de runtime capturadas.
