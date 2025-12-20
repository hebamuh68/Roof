from app.models.apartment_pyd import ApartmentFilter
from app.services.es_client import es

def search_apartments(
        query: str,
        fuzziness: str = "AUTO",
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "relevance"
) -> dict:
    
    # Build the query
    es_query = {
        "multi_match": {
            "query": query,
            "fields": ["title^3", "description^2", "location^2", "keywords"],
            "fuzziness": fuzziness,
            "prefix_length": 2,
            "max_expansions": 50,
            "type": "best_fields"
        }
    }

    # Build sort based on option
    sort_config = None
    if sort_by == "price_asc":
        sort_config = [{"rent_per_week": "asc"}]
    elif sort_by == "price_desc":
        sort_config = [{"rent_per_week": "desc"}]
    elif sort_by == "date_desc":
        sort_config = [{"created_at": "desc"}]
    elif sort_by == "date_asc":
        sort_config = [{"created_at": "asc"}]
    elif sort_by == "views_desc":
        sort_config = [{"view_count": "desc"}]
    elif sort_by == "featured":
        sort_config = [
            {"is_featured": {"order": "desc"}},
            {"featured_priority": {"order": "desc"}},
            "_score" # Then by relevance
        ]

    # Execute search with separate parameters
    search_params = {
        "index": "apartments",
        "query": es_query,
        "from_": skip,
        "size": limit
    }

    if sort_config:
        search_params["sort"] = sort_config

    return es.search(**search_params)

def filter_apartments(apartment: ApartmentFilter, sort_by: str = "date_desc") -> dict:

    # Must queries for filtering
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


    # Should queries for filtering
    should_queries = []
    if apartment.keywords:
        should_queries.append({
            "multi_match": {
                "query": " ".join(apartment.keywords),
                "fields": ["title", "description", "keywords"]
            }
        })
    
    # Build the bool query
    es_query = {
        "bool": {
            "must": must_queries,
            "should": should_queries
        }
    }

    # Build sort config
    sort_config = None
    if sort_by == "price_asc":
        sort_config = [{"rent_per_week": "asc"}]
    elif sort_by == "price_desc":
        sort_config = [{"rent_per_week": "desc"}]
    elif sort_by == "date_desc":
        sort_config = [{"created_at": "desc"}]
    elif sort_by == "date_asc":
        sort_config = [{"created_at": "asc"}]

    # Execute search with separate parameters
    search_params = {
        "index": "apartments",
        "query": es_query
    }

    if sort_config:
        search_params["sort"] = sort_config

    return es.search(**search_params)

def suggest_spelling(query: str, max_suggestions: int = 5) -> list[str]:
    """
    Get spelling suggestions for potentially misspelled queries using Elasticsearch term suggester.

    Args:
        query: The search query that may contain typos
        max_suggestions: Maximum number of suggestions to return

    Returns:
        List of suggested corrections
    """
    try:
        # Use Elasticsearch suggest API for term suggestions
        suggest_body = {
            "text": query,
            "title_suggest": {
                "term": {
                    "field": "title",
                    "size": max_suggestions,
                    "suggest_mode": "popular",
                    "min_word_length": 3,
                    "prefix_length": 1
                }
            },
            "description_suggest": {
                "term": {
                    "field": "description",
                    "size": max_suggestions,
                    "suggest_mode": "popular",
                    "min_word_length": 3,
                    "prefix_length": 1
                }
            },
            "location_suggest": {
                "term": {
                    "field": "location",
                    "size": max_suggestions,
                    "suggest_mode": "popular",
                    "min_word_length": 3,
                    "prefix_length": 1
                }
            }
        }

        # Execute suggestion query
        response = es.search(
            index="apartments",
            suggest=suggest_body,
            size=0  # We don't need search results, just suggestions
        )

        # Extract unique suggestions from all fields
        suggestions = set()

        if "suggest" in response:
            for field_name, field_suggestions in response["suggest"].items():
                for suggestion_group in field_suggestions:
                    for option in suggestion_group.get("options", []):
                        suggestions.add(option["text"])

        # Return as sorted list
        return sorted(list(suggestions))[:max_suggestions]

    except Exception as e:
        # Log error and return empty list
        print(f"Error getting spelling suggestions: {e}")
        return []


def autocomplete_suggestions(
    query: str,
    field: str = "all",
    limit: int = 10
) -> dict:
    """
    Get autocomplete suggestions as user types.

    Args:
        query: Partial search query
        field: Which field to autocomplete from (all, title, location, keywords)
        limit: Maximum number of suggestions

    Returns:
        Dict with suggestions grouped by field type
    """
    try:
        suggestions_dict = {
            "titles": [],
            "locations": [],
            "keywords": []
        }

        # Build suggest query based on field parameter
        suggest_fields = {}

        if field in ["all", "title"]:
            suggest_fields["title_completions"] = {
                "prefix": query,
                "completion": {
                    "field": "title.suggest",
                    "size": limit,
                    "skip_duplicates": True
                }
            }

        if field in ["all", "location"]:
            suggest_fields["location_completions"] = {
                "prefix": query,
                "completion": {
                    "field": "location.suggest",
                    "size": limit,
                    "skip_duplicates": True
                }
            }

        if field in ["all", "keywords"]:
            suggest_fields["keyword_completions"] = {
                "prefix": query,
                "completion": {
                    "field": "keywords.suggest",
                    "size": limit,
                    "skip_duplicates": True
                }
            }

        # Execute autocomplete query
        response = es.search(
            index="apartments",
            suggest=suggest_fields,
            size=0  # We only need suggestions, not search results
        )

        # Extract suggestions from response
        if "suggest" in response:
            # Process title suggestions
            if "title_completions" in response["suggest"]:
                for suggestion_group in response["suggest"]["title_completions"]:
                    for option in suggestion_group.get("options", []):
                        suggestions_dict["titles"].append(option["text"])

            # Process location suggestions
            if "location_completions" in response["suggest"]:
                for suggestion_group in response["suggest"]["location_completions"]:
                    for option in suggestion_group.get("options", []):
                        suggestions_dict["locations"].append(option["text"])

            # Process keyword suggestions
            if "keyword_completions" in response["suggest"]:
                for suggestion_group in response["suggest"]["keyword_completions"]:
                    for option in suggestion_group.get("options", []):
                        suggestions_dict["keywords"].append(option["text"])

        return suggestions_dict

    except Exception as e:
        print(f"Error getting autocomplete suggestions: {e}")
        return {"titles": [], "locations": [], "keywords": []}
