from elasticsearch import Elasticsearch
import os

ELASTIC_URL = os.getenv("ELASTIC_URL", "http://localhost:9200")

# Create Elasticsearch client
es = Elasticsearch(ELASTIC_URL)