"""
SEO CLI - Skill①: Hot Word Collection
Collect trending keywords from multiple sources
"""

import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import logging
from typing import List, Dict
from external.searxng import SearXNGClient
from external.trends import TrendsClient

logger = logging.getLogger(__name__)

def collect_hot_words(date=None, limit=100, timeout=10) -> List[str]:
    """
    Collect hot/trending keywords from multiple sources

    Args:
        date: Target date (not used in current implementation)
        limit: Maximum number of keywords to collect
        timeout: Request timeout in seconds

    Returns:
        List of trending keywords
    """
    logger.info(f"Collecting hot words (limit: {limit})")

    all_keywords = []

    # Source 1: SearXNG trending searches
    try:
        logger.info("Fetching from SearXNG...")
        searxng_client = SearXNGClient(timeout=timeout)
        if searxng_client.health_check():
            trending_keywords = searxng_client.search_trending_topics()
            all_keywords.extend(trending_keywords)
            logger.info(f"Collected {len(trending_keywords)} keywords from SearXNG")
        else:
            logger.warning("SearXNG is not available")
    except Exception as e:
        logger.error(f"Error collecting from SearXNG: {e}")

    # Source 2: Google Trends RSS (if available)
    try:
        logger.info("Fetching from Google Trends RSS...")
        trends_keywords = collect_from_google_trends_rss(timeout=timeout)
        all_keywords.extend(trends_keywords)
        logger.info(f"Collected {len(trends_keywords)} keywords from Google Trends RSS")
    except Exception as e:
        logger.error(f"Error collecting from Google Trends RSS: {e}")

    # Source 3: Generic trending searches
    try:
        logger.info("Performing generic trending searches...")
        generic_keywords = collect_from_generic_searches(timeout=timeout)
        all_keywords.extend(generic_keywords)
        logger.info(f"Collected {len(generic_keywords)} keywords from generic searches")
    except Exception as e:
        logger.error(f"Error collecting from generic searches: {e}")

    # Filter and deduplicate keywords
    filtered_keywords = filter_keywords(all_keywords)

    # Get top keywords by frequency
    top_keywords = get_top_keywords(filtered_keywords, limit)

    logger.info(f"Total unique keywords after filtering: {len(top_keywords)}")

    return top_keywords

def collect_from_google_trends_rss(timeout=10) -> List[str]:
    """Collect keywords from Google Trends RSS feeds"""
    keywords = []

    # Google Trends RSS URLs (these may change or be rate-limited)
    rss_urls = [
        "https://trends.google.com/trending/searches/daily/rss?geo=US",
        "https://trends.google.com/trending/searches/daily/rss?geo=GB",
    ]

    for url in rss_urls:
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                titles = soup.find_all('title')

                for title in titles[1:]:  # Skip the first title (RSS title)
                    text = title.get_text()
                    # Extract English words and phrases
                    words = extract_keywords_from_text(text)
                    keywords.extend(words)

        except Exception as e:
            logger.warning(f"Failed to fetch from {url}: {e}")
            continue

    return keywords

def collect_from_generic_searches(timeout=10) -> List[str]:
    """Collect keywords using generic trending queries"""
    keywords = []

    # Try to use SearXNG for generic trending queries
    try:
        searxng_client = SearXNGClient(timeout=timeout)
        if searxng_client.health_check():
            trending_queries = [
                "what's trending",
                "popular searches",
                "viral topics",
                "hot keywords",
                "trending now"
            ]

            for query in trending_queries:
                results = searxng_client.search(query, limit=10)
                keywords.extend(results)
    except Exception as e:
        logger.error(f"Error in generic searches: {e}")

    return keywords

def extract_keywords_from_text(text: str) -> List[str]:
    """Extract potential keywords from text"""
    # Convert to lowercase
    text = text.lower()

    # Extract English words (3+ characters)
    words = re.findall(r'\b[a-z]{3,}\b', text)

    # Filter out common stop words
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
        'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
        'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
        'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'
    }

    keywords = [word for word in words if word not in stop_words]

    return keywords

def filter_keywords(keywords: List[str]) -> List[str]:
    """Filter and clean keyword list"""
    filtered = []

    for keyword in keywords:
        # Clean the keyword
        keyword = keyword.strip().lower()

        # Skip if too short or too long
        if len(keyword) < 3 or len(keyword) > 50:
            continue

        # Skip if contains only numbers or special characters
        if not re.search(r'[a-z]', keyword):
            continue

        # Skip if it's a common non-keyword
        if keyword in {'the', 'and', 'for', 'are', 'but', 'not'}:
            continue

        filtered.append(keyword)

    return filtered

def get_top_keywords(keywords: List[str], limit: int) -> List[str]:
    """Get top N keywords by frequency"""
    # Count keyword frequencies
    word_counts = Counter(keywords)

    # Get most common keywords
    top_words = [word for word, count in word_counts.most_common(limit)]

    return top_words

def save_keywords_to_db(keywords: List[str], db):
    """Save keywords to database"""
    if not keywords:
        return

    logger.info(f"Saving {len(keywords)} keywords to database")

    for keyword in keywords:
        db.save_keyword(keyword)

    logger.info("Keywords saved successfully")
