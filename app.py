from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
import os

# Retrieve OpenTelemetry endpoint from environment variables
otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")

# Initialize tracing and set up the tracer provider
resource = Resource(attributes={"service.name": "flask-sample"})
trace.set_tracer_provider(TracerProvider(resource=resource))

# Configure the OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint=otel_endpoint, insecure=True)

# Add a BatchSpanProcessor to send spans in batches
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Initialize Flask app
app = Flask(__name__)

# Automatically instrument Flask and HTTP client libraries
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route("/")
def index():
    return "Hello, OpenTelemetry!"

@app.route("/trace")
def create_trace():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("sample-trace"):
        return "Trace created!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
