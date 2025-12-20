from app.services.es_client import es

index_body = {
    "mappings": {
        "properties": {
            "title": {
                "type": "text",  # searchable with relevance scoring
                "fields": {
                    "suggest": {
                        "type": "completion"  # for autocomplete
                    }
                }
            },
            "description": {"type": "text"},
            "location": {
                "type": "keyword",  # exact matches & filtering
                "fields": {
                    "suggest": {
                        "type": "completion"  # for autocomplete
                    }
                }
            },
            "apartment_type": {"type": "keyword"},
            "rent_per_week": {"type": "integer"},
            "start_date": {"type": "date"},  # store as date for range queries
            "duration_len": {"type": "integer"},
            "place_accept": {"type": "keyword"},
            "furnishing_type": {"type": "keyword"},
            "is_pathroom_solo": {"type": "boolean"},
            "parking_type": {"type": "keyword"},
            "keywords": {
                "type": "keyword",  # exact term matches
                "fields": {
                    "suggest": {
                        "type": "completion"  # for autocomplete
                    }
                }
            },
            "is_active": {"type": "boolean"}
        }
    }
}


# Create the index
if not es.indices.exists(index="apartments"):
    es.indices.create(index="apartments", mappings=index_body["mappings"])
    print("✅ Elasticsearch index 'apartments' created successfully.")
else:
    print("✅ Elasticsearch index 'apartments' already exists.")
