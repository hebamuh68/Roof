from app.services.es_client import es

index_body = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},  # searchable with relevance scoring
            "description": {"type": "text"},
            "location": {"type": "keyword"},  # exact matches & filtering
            "apartment_type": {"type": "keyword"},
            "rent_per_week": {"type": "integer"},
            "start_date": {"type": "date"},  # store as date for range queries
            "duration_len": {"type": "integer"},
            "place_accept": {"type": "keyword"},
            "furnishing_type": {"type": "keyword"},
            "is_pathroom_solo": {"type": "boolean"},
            "parking_type": {"type": "keyword"},
            "keywords": {"type": "keyword"},  # exact term matches
            "is_active": {"type": "boolean"}
        }
    }
}


# Create the index
es.indices.create(index="apartments", body=index_body, ignore=400)
print("✅ Elasticsearch index 'apartments' created or already exists.")
