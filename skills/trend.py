"""
SEO CLI - Skill②: Trend Verification
Verify keyword trends using Google Trends data
"""

import logging
from typing import List, Dict
from external.trends import TrendsClient

logger = logging.getLogger(__name__)

def verify_trends(keywords: List[str], timeout: int = 10) -> List[Dict]:
    """
    Verify trends for a list of keywords using Google Trends

    Args:
        keywords: List of keywords to verify
        timeout: Request timeout in seconds

    Returns:
        List of verified keywords with trend data
    """
    if not keywords:
        logger.warning("No keywords provided for trend verification")
        return []

    logger.info(f"Verifying trends for {len(keywords)} keywords")

    # Initialize trends client
    trends_client = TrendsClient(timeout=timeout)

    if not trends_client.init():
        logger.error("Failed to initialize PyTrends client")
        return []

    # Process keywords in batches to avoid rate limiting
    batch_size = 5
    verified_keywords = []

    for i in range(0, len(keywords), batch_size):
        batch = keywords[i:i + batch_size]
        logger.info(f"Processing batch {i // batch_size + 1}/{(len(keywords) - 1) // batch_size + 1}")

        try:
            # Get batch trend data
            batch_data = trends_client.get_batch_trend_data(batch)

            for keyword in batch:
                if keyword in batch_data and batch_data[keyword]:
                    trend_data = batch_data[keyword]
                    verified_keywords.append({
                        'word': keyword,
                        'search_volume': trend_data.get('avg_volume', 0),
                        'max_volume': trend_data.get('max_volume', 0),
                        'trend_score': trend_data.get('trend_score', 0),
                        'is_rising': trend_data.get('is_rising', False)
                    })
                    logger.debug(f"Verified trend for '{keyword}': score={trend_data.get('trend_score', 0)}")
                else:
                    # Add keyword with no trend data
                    verified_keywords.append({
                        'word': keyword,
                        'search_volume': 0,
                        'max_volume': 0,
                        'trend_score': 0,
                        'is_rising': False
                    })
                    logger.debug(f"No trend data found for '{keyword}'")

        except Exception as e:
            logger.error(f"Error processing batch: {e}")
            continue

    # Filter keywords with valid trend data
    valid_keywords = [kw for kw in verified_keywords if kw['search_volume'] > 0]

    logger.info(f"Trend verification complete: {len(valid_keywords)}/{len(keywords)} keywords have valid data")

    # Sort by trend score (descending)
    valid_keywords.sort(key=lambda x: x['trend_score'], reverse=True)

    return valid_keywords

def calculate_trend_score(time_series) -> float:
    """
    Calculate trend score (0-100) based on time series data

    Args:
        time_series: Pandas Series with time series data

    Returns:
        Trend score (0-100)
    """
    if len(time_series) == 0:
        return 0.0

    try:
        # Calculate recent average (last 30 days)
        recent_avg = time_series.tail(30).mean()

        # Calculate peak value
        peak_value = time_series.max()

        # Calculate score
        if peak_value > 0:
            score = (recent_avg / peak_value) * 100
            return round(min(score, 100), 2)

        return 0.0

    except Exception as e:
        logger.error(f"Error calculating trend score: {e}")
        return 0.0

def is_rising_trend(time_series) -> bool:
    """
    Check if a trend is rising

    Args:
        time_series: Pandas Series with time series data

    Returns:
        True if trend is rising, False otherwise
    """
    if len(time_series) < 14:
        return False

    try:
        # Calculate average for last 7 days
        recent = time_series.tail(7).mean()

        # Calculate average for previous 7 days
        previous = time_series.tail(14).head(7).mean()

        # Consider it rising if recent is 20% higher than previous
        return recent > previous * 1.2

    except Exception as e:
        logger.error(f"Error checking rising trend: {e}")
        return False

def get_trend_category(trend_score: float) -> str:
    """
    Categorize trend based on score

    Args:
        trend_score: Trend score (0-100)

    Returns:
        Category string: 'hot', 'rising', 'stable', or 'declining'
    """
    if trend_score >= 70:
        return 'hot'
    elif trend_score >= 40:
        return 'rising'
    elif trend_score >= 20:
        return 'stable'
    else:
        return 'declining'

def estimate_search_volume(trend_score: float, max_volume: int) -> int:
    """
    Estimate search volume based on trend score and max volume

    Args:
        trend_score: Trend score (0-100)
        max_volume: Maximum volume from trends data

    Returns:
        Estimated search volume
    """
    # Simple estimation based on trend score and max volume
    # This is a rough approximation
    if trend_score >= 70:
        return int(max_volume * 0.8)
    elif trend_score >= 40:
        return int(max_volume * 0.5)
    elif trend_score >= 20:
        return int(max_volume * 0.3)
    else:
        return int(max_volume * 0.1)

def filter_trending_keywords(verified_keywords: List[Dict], min_score: float = 20.0) -> List[Dict]:
    """
    Filter keywords based on minimum trend score

    Args:
        verified_keywords: List of verified keywords
        min_score: Minimum trend score threshold

    Returns:
        Filtered list of keywords
    """
    filtered = [kw for kw in verified_keywords if kw['trend_score'] >= min_score]

    logger.info(f"Filtered {len(filtered)}/{len(verified_keywords)} keywords with score >= {min_score}")

    return filtered

def get_top_trending_keywords(verified_keywords: List[Dict], limit: int = 20) -> List[Dict]:
    """
    Get top N trending keywords

    Args:
        verified_keywords: List of verified keywords
        limit: Maximum number of keywords to return

    Returns:
        Top trending keywords
    """
    # Sort by trend score (descending)
    sorted_keywords = sorted(verified_keywords, key=lambda x: x['trend_score'], reverse=True)

    return sorted_keywords[:limit]
