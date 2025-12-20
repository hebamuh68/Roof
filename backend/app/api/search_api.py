from fastapi import APIRouter, Query
from app.models.apartment_pyd import ApartmentFilter, SortOption
from app.services import search_service

router = APIRouter()

@router.get("/search/apartments")
def search(
    query: str = Query(..., min_length=1, description="Search query string"),
    fuzziness: str = Query("AUTO", regex="^(AUTO|0|1|2)$", description="Fuzzy matching level"),
    sort_by: SortOption = Query(SortOption.RELEVANCE, description="Sort order"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Full-text search with fuzzy matching support.

    Fuzziness options:
    - AUTO: Automatic edit distance (recommended)
    - 0: Exact match only
    - 1: Allow 1 character difference
    - 2: Allow 2 character differences
    """
    results = search_service.search_apartments(query, fuzziness, skip, limit, sort_by.value)
    return results["hits"]["hits"]

@router.post("/filter/apartments")
def filter_apartments(
    apartment: ApartmentFilter,
    sort_by: SortOption = Query(SortOption.DATE_NEWEST)
):
    results = search_service.filter_apartments(apartment, sort_by.value)
    return [hit["_source"] for hit in results["hits"]["hits"]]

@router.get("/search/suggestions")
def spelling_suggestions(
    query: str = Query(..., min_length=3, description="Query to check spelling")
):
    """Get spelling suggestions for potentially misspelled queries."""
    suggestions = search_service.suggest_spelling(query)
    return {"suggestions": suggestions}

@router.get("/autocomplete")
def autocomplete(
    query: str = Query(..., min_length=1, max_length=100, description="Partial search query"),
    field: str = Query("all", regex="^(all|title|location|keywords)$", description="Field to autocomplete"),
    limit: int = Query(10, ge=1, le=50, description="Maximum suggestions")
):
    """
    Get autocomplete suggestions as user types.

    Returns suggestions from titles, locations, and keywords based on the field parameter.
    """
    return search_service.autocomplete_suggestions(query, field, limit)