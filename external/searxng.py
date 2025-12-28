"""
SEO CLI - SearXNG Client
Local search engine wrapper for keyword discovery
"""

import requests
import logging
from typing import List, Dict, Optional
from urllib.parse import quote
import time
import random

logger = logging.getLogger(__name__)

class SearXNGClient:
    """Client for interacting with local SearXNG instance"""

    def __init__(self, base_url: str = "http://localhost:8080", timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def health_check(self) -> bool:
        """Check if SearXNG is running and healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"SearXNG health check failed: {e}")
            return False

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Perform a search query"""
        try:
            params = {
                'q': query,
                'format': 'json',
                'pageno': 1,
                'time_range': 'month'
            }

            response = requests.get(
                f"{self.base_url}/search",
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])

                # Extract keywords from search results
                keywords = []
                for result in results[:limit]:
                    title = result.get('title', '')
                    content = result.get('content', '')
                    # Simple keyword extraction from title and content
                    text = f"{title} {content}".lower()

                    # Extract potential keywords (simple approach)
                    words = text.split()
                    for word in words:
                        word = word.strip('.,!?()[]{}"\'-').lower()
                        if len(word) > 3 and word.isalpha():
                            keywords.append(word)

                # Remove duplicates while preserving order
                unique_keywords = []
                seen = set()
                for keyword in keywords:
                    if keyword not in seen:
                        unique_keywords.append(keyword)
                        seen.add(keyword)

                return unique_keywords[:limit * 2]  # Return more keywords for filtering

            else:
                logger.error(f"SearXNG search failed with status {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    def search_trending_topics(self, category: str = "general") -> List[str]:
        """Search for trending topics"""
        # Try to get trending topics through search
        trending_queries = [
            "trending today",
            "popular now",
            "viral topics",
            "hot news",
            "latest trends"
        ]

        all_keywords = []

        for query in trending_queries:
            keywords = self.search(query, limit=20)
            all_keywords.extend(keywords)
            time.sleep(random.uniform(0.5, 1.5))  # Avoid rate limiting

        # Return unique keywords
        return list(set(all_keywords))

    def get_related_searches(self, query: str) -> List[str]:
        """Get related search terms"""
        try:
            # Perform search and extract related terms from results
            results = self.search(query, limit=15)

            # Extract potential related keywords
            related = []
            for keyword in results:
                if keyword.lower() != query.lower():
                    related.append(keyword)

            return related[:10]

        except Exception as e:
            logger.error(f"Error getting related searches: {e}")
            return []
