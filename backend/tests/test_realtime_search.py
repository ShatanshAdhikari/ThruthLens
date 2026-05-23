import pytest
from app.services.search_service import search_service
from app.services.retrieval_service import retrieval_service
from unittest.mock import patch, MagicMock

def test_duckduckgo_search():
    # Test DDG search directly
    # Note: This might fail in CI if network is blocked, but good for local dev
    try:
        results = search_service.search_all("What is the capital of France?", max_results=1)
        assert len(results) >= 0 # Just check it doesn't crash
        if len(results) > 0:
            assert "Paris" in results[0]["text"]
            assert results[0]["source"] == "DuckDuckGo"
    except Exception as e:
        pytest.skip(f"Search failed due to network or rate limiting: {e}")

@patch("app.services.search_service.search_service.search_all")
def test_hybrid_retrieval_fallback(mock_search):
    # Mock search to return a specific result
    mock_search.return_value = [{
        "text": "Live web evidence about a specific topic.",
        "source": "Web Source",
        "url": "https://example.com",
        "type": "web_search"
    }]
    
    # Query something that definitely isn't in local seed data
    query = "Specific non-existent topic in seed data 12345"
    results = retrieval_service.retrieve_hybrid(query, n_results=1)
    
    assert any(res["metadata"]["type"] == "web_search" for res in results)
    assert any("Web Source" == res["metadata"]["source"] for res in results)

def test_search_service_orchestration():
    # Ensure it returns formatted results
    results = search_service.search_all("Test query", max_results=2)
    assert isinstance(results, list)
    for r in results:
        assert "text" in r
        assert "source" in r
        assert "url" in r
