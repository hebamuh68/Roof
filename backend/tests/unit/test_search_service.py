import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.search_service import (
    search_apartments,
    filter_apartments,
    suggest_spelling,
    autocomplete_suggestions
)
from app.models.apartment_pyd import ApartmentFilter


class TestSearchService:
    """Test suite for search service operations."""

    @patch('app.services.search_service.es')
    def test_search_apartments_basic(self, mock_es):
        """Test basic apartment search."""
        # Arrange
        mock_response = {
            "hits": {
                "total": {"value": 2},
                "hits": [
                    {"_id": "1", "_source": {"title": "Apartment 1"}},
                    {"_id": "2", "_source": {"title": "Apartment 2"}}
                ]
            }
        }
        mock_es.search.return_value = mock_response

        # Act
        result = search_apartments("sydney apartment", limit=10)

        # Assert
        assert result == mock_response
        mock_es.search.assert_called_once()
        call_args = mock_es.search.call_args
        assert call_args[1]["index"] == "apartments"
        assert call_args[1]["from_"] == 0
        assert call_args[1]["size"] == 10

    @patch('app.services.search_service.es')
    def test_search_apartments_with_pagination(self, mock_es):
        """Test search with pagination."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}

        # Act
        search_apartments("test", skip=10, limit=20)

        # Assert
        call_args = mock_es.search.call_args
        assert call_args[1]["from_"] == 10
        assert call_args[1]["size"] == 20

    @patch('app.services.search_service.es')
    def test_search_apartments_with_fuzziness(self, mock_es):
        """Test search with different fuzziness levels."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}

        # Act
        search_apartments("sydney", fuzziness="1")

        # Assert
        call_args = mock_es.search.call_args
        query = call_args[1]["query"]
        assert query["multi_match"]["fuzziness"] == "1"

    @patch('app.services.search_service.es')
    def test_search_apartments_sort_by_price_asc(self, mock_es):
        """Test search sorted by price ascending."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}

        # Act
        search_apartments("test", sort_by="price_asc")

        # Assert
        call_args = mock_es.search.call_args
        assert "sort" in call_args[1]
        assert call_args[1]["sort"] == [{"rent_per_week": "asc"}]

    @patch('app.services.search_service.es')
    def test_search_apartments_sort_by_price_desc(self, mock_es):
        """Test search sorted by price descending."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}

        # Act
        search_apartments("test", sort_by="price_desc")

        # Assert
        call_args = mock_es.search.call_args
        assert call_args[1]["sort"] == [{"rent_per_week": "desc"}]

    @patch('app.services.search_service.es')
    def test_search_apartments_sort_by_date_desc(self, mock_es):
        """Test search sorted by date descending."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}

        # Act
        search_apartments("test", sort_by="date_desc")

        # Assert
        call_args = mock_es.search.call_args
        assert call_args[1]["sort"] == [{"created_at": "desc"}]

    @patch('app.services.search_service.es')
    def test_search_apartments_sort_by_views_desc(self, mock_es):
        """Test search sorted by views descending."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}

        # Act
        search_apartments("test", sort_by="views_desc")

        # Assert
        call_args = mock_es.search.call_args
        assert call_args[1]["sort"] == [{"view_count": "desc"}]

    @patch('app.services.search_service.es')
    def test_search_apartments_sort_by_featured(self, mock_es):
        """Test search sorted by featured status."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}

        # Act
        search_apartments("test", sort_by="featured")

        # Assert
        call_args = mock_es.search.call_args
        sort_config = call_args[1]["sort"]
        assert len(sort_config) == 3
        assert sort_config[0] == {"is_featured": {"order": "desc"}}
        assert sort_config[1] == {"featured_priority": {"order": "desc"}}
        assert sort_config[2] == "_score"

    @patch('app.services.search_service.es')
    def test_search_apartments_default_relevance(self, mock_es):
        """Test default search uses relevance (no sort)."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}

        # Act
        search_apartments("test", sort_by="relevance")

        # Assert
        call_args = mock_es.search.call_args
        assert "sort" not in call_args[1] or call_args[1].get("sort") is None

    @patch('app.services.search_service.es')
    def test_filter_apartments_basic(self, mock_es):
        """Test basic apartment filtering."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}
        filter_data = ApartmentFilter(
            location="Sydney",
            apartment_type="Studio",
            rent_per_week=500
        )

        # Act
        filter_apartments(filter_data)

        # Assert
        mock_es.search.assert_called_once()
        call_args = mock_es.search.call_args
        query = call_args[1]["query"]
        assert "bool" in query
        assert "must" in query["bool"]

    @patch('app.services.search_service.es')
    def test_filter_apartments_with_location(self, mock_es):
        """Test filtering by location."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}
        filter_data = ApartmentFilter(location="Melbourne")

        # Act
        filter_apartments(filter_data)

        # Assert
        call_args = mock_es.search.call_args
        query = call_args[1]["query"]
        must_queries = query["bool"]["must"]
        location_match = [q for q in must_queries if "match" in q and "location" in q["match"]]
        assert len(location_match) > 0

    @patch('app.services.search_service.es')
    def test_filter_apartments_with_price_range(self, mock_es):
        """Test filtering by price range."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}
        filter_data = ApartmentFilter(rent_per_week=500)

        # Act
        filter_apartments(filter_data)

        # Assert
        call_args = mock_es.search.call_args
        query = call_args[1]["query"]
        must_queries = query["bool"]["must"]
        price_range = [q for q in must_queries if "range" in q and "rent_per_week" in q["range"]]
        assert len(price_range) > 0
        assert price_range[0]["range"]["rent_per_week"]["lte"] == 500

    @patch('app.services.search_service.es')
    def test_filter_apartments_with_keywords(self, mock_es):
        """Test filtering with keywords (should queries)."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}
        filter_data = ApartmentFilter(keywords=["pet-friendly", "parking"])

        # Act
        filter_apartments(filter_data)

        # Assert
        call_args = mock_es.search.call_args
        query = call_args[1]["query"]
        should_queries = query["bool"].get("should", [])
        assert len(should_queries) > 0

    @patch('app.services.search_service.es')
    def test_filter_apartments_with_multiple_filters(self, mock_es):
        """Test filtering with multiple criteria."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}
        filter_data = ApartmentFilter(
            location="Sydney",
            apartment_type="1BHK",
            rent_per_week=600,
            furnishing_type="Furnished",
            is_pathroom_solo=True
        )

        # Act
        filter_apartments(filter_data)

        # Assert
        call_args = mock_es.search.call_args
        query = call_args[1]["query"]
        must_queries = query["bool"]["must"]
        # Should have status, is_active, location, type, price, furnishing, bathroom
        assert len(must_queries) >= 7

    @patch('app.services.search_service.es')
    def test_filter_apartments_sort_by_price(self, mock_es):
        """Test filter with price sorting."""
        # Arrange
        mock_es.search.return_value = {"hits": {"total": {"value": 0}, "hits": []}}
        filter_data = ApartmentFilter()

        # Act
        filter_apartments(filter_data, sort_by="price_asc")

        # Assert
        call_args = mock_es.search.call_args
        assert "sort" in call_args[1]
        assert call_args[1]["sort"] == [{"rent_per_week": "asc"}]

    @patch('app.services.search_service.es')
    def test_suggest_spelling_success(self, mock_es):
        """Test spelling suggestions."""
        # Arrange
        mock_response = {
            "suggest": {
                "title_suggest": [
                    {
                        "options": [
                            {"text": "sydney"},
                            {"text": "sydeny"}
                        ]
                    }
                ]
            }
        }
        mock_es.search.return_value = mock_response

        # Act
        suggestions = suggest_spelling("sydeny", max_suggestions=5)

        # Assert
        assert len(suggestions) > 0
        assert "sydney" in suggestions
        mock_es.search.assert_called_once()
        call_args = mock_es.search.call_args
        assert call_args[1]["size"] == 0  # No search results needed

    @patch('app.services.search_service.es')
    def test_suggest_spelling_empty(self, mock_es):
        """Test spelling suggestions with no suggestions."""
        # Arrange
        mock_es.search.return_value = {"suggest": {}}

        # Act
        suggestions = suggest_spelling("xyzabc", max_suggestions=5)

        # Assert
        assert suggestions == []

    @patch('app.services.search_service.es')
    def test_suggest_spelling_error_handling(self, mock_es):
        """Test spelling suggestions error handling."""
        # Arrange
        mock_es.search.side_effect = Exception("Elasticsearch error")

        # Act
        suggestions = suggest_spelling("test")

        # Assert
        assert suggestions == []

    @patch('app.services.search_service.es')
    def test_autocomplete_suggestions_all_fields(self, mock_es):
        """Test autocomplete for all fields."""
        # Arrange
        mock_response = {
            "suggest": {
                "title_completions": [
                    {"options": [{"text": "Sydney Apartment"}]}
                ],
                "location_completions": [
                    {"options": [{"text": "Sydney"}]}
                ],
                "keyword_completions": [
                    {"options": [{"text": "pet-friendly"}]}
                ]
            }
        }
        mock_es.search.return_value = mock_response

        # Act
        result = autocomplete_suggestions("syd", field="all")

        # Assert
        assert "titles" in result
        assert "locations" in result
        assert "keywords" in result
        assert len(result["titles"]) > 0
        assert len(result["locations"]) > 0

    @patch('app.services.search_service.es')
    def test_autocomplete_suggestions_title_only(self, mock_es):
        """Test autocomplete for title field only."""
        # Arrange
        mock_response = {
            "suggest": {
                "title_completions": [
                    {"options": [{"text": "Sydney Apartment"}]}
                ]
            }
        }
        mock_es.search.return_value = mock_response

        # Act
        result = autocomplete_suggestions("syd", field="title")

        # Assert
        assert "titles" in result
        assert len(result["titles"]) > 0
        assert len(result["locations"]) == 0
        assert len(result["keywords"]) == 0

    @patch('app.services.search_service.es')
    def test_autocomplete_suggestions_error_handling(self, mock_es):
        """Test autocomplete error handling."""
        # Arrange
        mock_es.search.side_effect = Exception("Elasticsearch error")

        # Act
        result = autocomplete_suggestions("test")

        # Assert
        assert result == {"titles": [], "locations": [], "keywords": []}

    @patch('app.services.search_service.es')
    def test_autocomplete_suggestions_with_limit(self, mock_es):
        """Test autocomplete with custom limit."""
        # Arrange
        mock_es.search.return_value = {"suggest": {}}

        # Act
        autocomplete_suggestions("test", limit=20)

        # Assert
        call_args = mock_es.search.call_args
        suggest_config = call_args[1]["suggest"]
        # Check that size is set in completion config
        assert "title_completions" in suggest_config or "location_completions" in suggest_config

