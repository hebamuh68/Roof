from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ELASTIC_URL = os.getenv("ELASTIC_URL", "http://localhost:9200")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

# Create Elasticsearch client with authentication if credentials provided
if ELASTIC_USER and ELASTIC_PASSWORD:
    es = Elasticsearch(
        ELASTIC_URL,
        basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
        verify_certs=False,  # For development
        ssl_show_warn=False
    )
else:
    # No authentication for development
    es = Elasticsearch(ELASTIC_URL)