from app.services.elasticsearch import es

def search_apartments(query: str):
    return es.search(
        index="apartments",
        body={
            "query": {
                "multi_match":{
                    "query": query,
                    "fields": ["title", "description", "location", "keywords"]
                }
            }
        }
    )