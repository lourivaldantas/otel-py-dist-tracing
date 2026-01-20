# --- OpenTelemetry ---
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# tracer
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

#logs
import logging
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider

def configure_opentelemetry():
    resource = Resource.create(attributes={
        SERVICE_NAME: "client-api"
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
