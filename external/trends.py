"""
SEO CLI - PyTrends Client
Google Trends wrapper with error handling and rate limiting
"""

import logging
from typing import Dict, List, Optional
from pytrends.request import TrendReq
import time
import random

logger = logging.getLogger(__name__)

class TrendsClient:
    """Client for Google Trends data with rate limiting"""

    def __init__(self, language: str = 'en-US', timeout: int = 10):
        self.language = language
        self.timeout = timeout
        self.pytrends = None
        self.last_request_time = 0
        self.min_delay = 1.0  # Minimum delay between requests

    def init(self) -> bool:
        """Initialize PyTrends client"""
        try:
            self.pytrends = TrendReq(hl=self.language, tz=360)
            logger.info("PyTrends client initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize PyTrends: {e}")
            return False

    def _rate_limit(self):
        """Apply rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.min_delay:
            sleep_time = self.min_delay - time_since_last
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def get_trend_data(self, keyword: str, timeframe: str = 'today 12-m') -> Dict:
        """Get trend data for a keyword"""
        if not self.pytrends:
            if not self.init():
                return {}

        self._rate_limit()

        try:
            # Build payload
            self.pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='', gprop='')

            # Get interest over time
            interest_over_time = self.pytrends.interest_over_time()

            if not interest_over_time.empty:
                # Calculate statistics
                data = {
                    'keyword': keyword,
                    'avg_volume': int(interest_over_time[keyword].mean()),
                    'max_volume': int(interest_over_time[keyword].max()),
                    'min_volume': int(interest_over_time[keyword].min()),
                    'trend_score': self._calculate_trend_score(interest_over_time[keyword]),
                    'is_rising': self._is_rising_trend(interest_over_time[keyword]),
                    'data_points': len(interest_over_time)
                }

                return data
            else:
                logger.warning(f"No trend data found for '{keyword}'")
                return {}

        except Exception as e:
            logger.error(f"Error getting trend data for '{keyword}': {e}")
            return {}

    def get_batch_trend_data(self, keywords: list, timeframe: str = 'today 12-m') -> Dict:
        """Get trend data for multiple keywords"""
        if not self.pytrends:
            if not self.init():
                return {}

        self._rate_limit()

        try:
            # Build payload for multiple keywords
            self.pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo='', gprop='')

            # Get interest over time
            interest_over_time = self.pytrends.interest_over_time()

            results = {}

            if not interest_over_time.empty:
                for keyword in keywords:
                    if keyword in interest_over_time.columns:
                        results[keyword] = {
                            'avg_volume': int(interest_over_time[keyword].mean()),
                            'max_volume': int(interest_over_time[keyword].max()),
                            'trend_score': self._calculate_trend_score(interest_over_time[keyword]),
                            'is_rising': self._is_rising_trend(interest_over_time[keyword])
                        }
                    else:
                        logger.warning(f"No data found for '{keyword}'")
                        results[keyword] = {}

            return results

        except Exception as e:
            logger.error(f"Error getting batch trend data: {e}")
            return {}

    def _calculate_trend_score(self, time_series) -> float:
        """Calculate trend score (0-100)"""
        if len(time_series) == 0:
            return 0.0

        # Simple scoring based on recent average vs peak
        recent_avg = time_series.tail(30).mean()
        peak_value = time_series.max()

        if peak_value > 0:
            score = (recent_avg / peak_value) * 100
            return round(score, 2)

        return 0.0

    def _is_rising_trend(self, time_series) -> bool:
        """Check if trend is rising"""
        if len(time_series) < 14:
            return False

        recent = time_series.tail(7).mean()
        previous = time_series.tail(14).head(7).mean()

        # Consider it rising if recent average is 20% higher
        return recent > previous * 1.2

    def get_related_queries(self, keyword: str) -> List[str]:
        """Get related queries for a keyword"""
        if not self.pytrends:
            if not self.init():
                return []

        self._rate_limit()

        try:
            self.pytrends.build_payload([keyword])

            # Get related queries
            related_queries = self.pytrends.related_queries()

            if keyword in related_queries:
                queries = related_queries[keyword]
                if 'top' in queries:
                    return [query['query'] for query in queries['top']['query'][:10]]

            return []

        except Exception as e:
            logger.error(f"Error getting related queries for '{keyword}': {e}")
            return []
