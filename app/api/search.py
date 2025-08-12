from fastapi import APIRouter, Query
from app.services.search_service import search_apartments

router = APIRouter()

@router.get("/search/apartments")
def search(query: str = Query(..., min_length=1, description="Search query string")):
    """
    Search apartments by query string.
    """
    results = search_apartments(query)
    # Return only the hits list inside the hits object
    return results["hits"]["hits"]
