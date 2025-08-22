from fastapi import APIRouter, Query
from app.models.apartment_pyd import ApartmentFilter
from app.services.search_service import search_apartments, filter_apartments

router = APIRouter()

@router.get("/search/apartments")
def search(query: str = Query(..., min_length=1, description="Search query string")):
    results = search_apartments(query)
    return results["hits"]["hits"]


@router.post("/filter/apartments")
def filter(apartment: ApartmentFilter):
    results = filter_apartments(apartment)
    return [hit["_source"]for hit in results["hits"]["hits"]]