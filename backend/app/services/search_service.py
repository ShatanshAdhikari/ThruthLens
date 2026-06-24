import requests
import time as _time
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, quote
from ddgs import DDGS
from tavily import TavilyClient
from app.config import settings
from abc import ABC, abstractmethod

_CACHE_TTL = 3600  # seconds


def _domain_from_url(url: str) -> str:
    try:
        netloc = urlparse(url).netloc
        return netloc.replace("www.", "") if netloc else url
    except Exception:
        return url

class BaseSearchSource(ABC):
    @abstractmethod
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        pass

class DuckDuckGoSearchSource(BaseSearchSource):
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        results = []
        try:
            with DDGS() as ddgs:
                ddg_results = list(ddgs.text(query, max_results=max_results))
                for r in ddg_results:
                    url = r.get("href", "")
                    results.append({
                        "text": r.get("body", ""),
                        "title": r.get("title", ""),
                        "source": _domain_from_url(url) if url else "DuckDuckGo",
                        "url": url,
                        "type": "web_search"
                    })
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
        return results

class TavilySearchSource(BaseSearchSource):
    def __init__(self, api_key: Optional[str]):
        self.client = TavilyClient(api_key=api_key) if api_key else None

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        if not self.client:
            return []
            
        results = []
        try:
            response = self.client.search(query, search_depth="advanced", max_results=max_results)
            for r in response.get("results", []):
                url = r.get("url", "")
                results.append({
                    "text": r.get("content", ""),
                    "title": r.get("title", ""),
                    "source": _domain_from_url(url) if url else "Tavily",
                    "url": url,
                    "type": "web_search"
                })
        except Exception as e:
            print(f"Tavily search error: {e}")
        return results

class WikipediaSearchSource(BaseSearchSource):
    _OPENSEARCH_URL = "https://en.wikipedia.org/w/api.php"
    _SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        results = []
        try:
            resp = requests.get(self._OPENSEARCH_URL, params={
                "action": "opensearch",
                "search": query,
                "limit": min(max_results, 3),
                "namespace": 0,
                "format": "json",
            }, timeout=6)
            if resp.status_code != 200:
                return results
            _, titles, _, urls = resp.json()
            for title, url in zip(titles, urls):
                s_resp = requests.get(
                    self._SUMMARY_URL.format(quote(title, safe="")),
                    timeout=6
                )
                if s_resp.status_code == 200:
                    data = s_resp.json()
                    extract = data.get("extract", "").strip()
                    if len(extract) >= 40:
                        results.append({
                            "text": extract[:600],
                            "title": title,
                            "source": "en.wikipedia.org",
                            "url": url,
                            "type": "encyclopedia",
                        })
        except Exception as e:
            print(f"Wikipedia search error: {e}")
        return results


class GoogleFactCheckSource(BaseSearchSource):
    def __init__(self, api_key: Optional[str]):
        self.api_key = api_key
        self.base_url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        if not self.api_key:
            return []
            
        results = []
        try:
            params = {
                "query": query,
                "key": self.api_key,
                "languageCode": "en",
                "pageSize": max_results
            }
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                claims = response.json().get("claims", [])
                for claim in claims:
                    review = claim.get("claimReview", [{}])[0]
                    publisher = review.get("publisher", {}).get("name", "Fact Check")
                    rating = review.get("textualRating", "Unknown")
                    
                    results.append({
                        "text": f"Claim: {claim.get('text')} | Rating: {rating} | Fact-checked by {publisher}",
                        "title": claim.get("text", ""),
                        "source": publisher,
                        "url": review.get("url", ""),
                        "type": "fact_check",
                        "rating": rating
                    })
        except Exception as e:
            print(f"Google Fact Check API error: {e}")
        return results

from app.services.ollama_service import ollama_service

class SearchService:
    def __init__(self):
        self.sources: List[BaseSearchSource] = []
        self._cache: Dict[str, Any] = {}

        if settings.TAVILY_API_KEY:
            self.sources.append(TavilySearchSource(settings.TAVILY_API_KEY))

        if settings.GOOGLE_FACT_CHECK_API_KEY:
            self.sources.append(GoogleFactCheckSource(settings.GOOGLE_FACT_CHECK_API_KEY))

        # Wikipedia — authoritative, free, no key required
        self.sources.append(WikipediaSearchSource())

        # DuckDuckGo as final fallback
        self.sources.append(DuckDuckGoSearchSource())

    def search_all(self, claim: str, context: Optional[str] = None, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Orchestrate multi-perspective search using LLM-generated queries.
        Results are cached per claim text for one hour.
        """
        cache_key = f"{claim}:{max_results}"
        cached = self._cache.get(cache_key)
        if cached:
            result, ts = cached
            if _time.time() - ts < _CACHE_TTL:
                return result

        queries = ollama_service.generate_search_queries(claim, context)

        all_results = []
        seen_urls: set = set()

        for query in queries:
            for source in self.sources:
                source_results = source.search(query, max_results=2)
                for res in source_results:
                    url = res.get("url") or ""
                    if url and url in seen_urls:
                        continue
                    all_results.append(res)
                    if url:
                        seen_urls.add(url)

                if len(all_results) >= max_results * 2:
                    break

        self._cache[cache_key] = (all_results, _time.time())
        return all_results

# Singleton instance
search_service = SearchService()
