from app.models.apartment_pyd import ApartmentFilter
from app.services.es_client import es

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

def filter_apartments(apartment: ApartmentFilter):
    must_queries = [
        {"term": {"status.keyword": "PUBLISHED"}},
        {"term": {"is_active": True}}
    ]
    if apartment.location:
        must_queries.append({"match": {"location": apartment.location}})
    if apartment.apartment_type:
        must_queries.append({"match": {"apartment_type": apartment.apartment_type}})
    if apartment.rent_per_week:
        must_queries.append({"range": {"rent_per_week": {"lte": apartment.rent_per_week}}})
    if apartment.start_date:
        must_queries.append({"range": {"start_date": {"gte": apartment.start_date}}})
    if apartment.duration_len:
        must_queries.append({"range": {"duration_len": {"gte": apartment.duration_len}}})
    if apartment.place_accept:
        must_queries.append({"match": {"place_accept": apartment.place_accept}})
    if apartment.furnishing_type:
        must_queries.append({"match": {"furnishing_type": apartment.furnishing_type}})
    if apartment.is_pathroom_solo is not None:
        must_queries.append({"term": {"is_pathroom_solo": apartment.is_pathroom_solo}})
    if apartment.parking_type:
        must_queries.append({"match": {"parking_type": apartment.parking_type}})


    should_queries = []
    if apartment.keywords:
        should_queries.append({
            "multi_match": {
                "query": " ".join(apartment.keywords),
                "fields": ["title", "description", "keywords"]
            }
        })

    
    return es.search(
        index="apartments",
        body={
            "query":{
                "bool":{
                    "must": must_queries,
                    "should": should_queries
                }
            }
        }
    )
