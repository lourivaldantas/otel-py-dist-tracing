import logging
import requests
from flask import Flask

# --- OpenTelemetry ---
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry import trace, metrics

# tracer
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

#logs
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider

def configure_opentelemetry():
    resource = Resource.create(attributes={
        SERVICE_NAME: "server-api"
    })

    # tracer configs
    tracerProvider = TracerProvider(resource=resource)
    tracerProcessor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces"))
    tracerProvider.add_span_processor(tracerProcessor)
    trace.set_tracer_provider(tracerProvider)

    # metrics configs
    metricsReader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://otel-collector:4318/v1/metrics")
    )
    meterProvider = MeterProvider(resource=resource, metric_readers=[metricsReader])
    metrics.set_meter_provider(meterProvider)

    # logs configs
    logProvider = LoggerProvider(resource=resource)
    logProcessor = BatchLogRecordProcessor(OTLPLogExporter(endpoint="http://otel-collector:4318/v1/logs"))
    logProvider.add_log_record_processor(logProcessor)
    set_logger_provider(logProvider)

    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logProvider)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

# --- API flask ---
configure_opentelemetry()
RequestsInstrumentor().instrument()

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
tracer = trace.get_tracer(__name__)

@app.route("/users")
@tracer.start_as_current_span("serverApi")


def serverApi():
    users = requests.get("https://jsonplaceholder.typicode.com/users").json()
    logging.info(f"Sucesso! {len(users)} usuários encontrados.")
    return users
