from elasticsearch import Elasticsearch
import os

ELASTIC_URL = os.getenv("ELASTIC_URL", "https://localhost:9200")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

# Create Elasticsearch client with authentication
es = Elasticsearch(
    ELASTIC_URL,
    basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
    verify_certs=False,  # For development
    ssl_show_warn=False
)