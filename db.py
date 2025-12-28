"""
SEO CLI - Database Module
SQLite database operations for keywords, plans, and search history
"""

import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    """SQLite database manager for SEO CLI"""

    def __init__(self, db_path: str = "./seo_cli.db"):
        self.db_path = Path(db_path)
        self.init_database()

    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create keywords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                search_volume INTEGER,
                trend_score REAL,
                intent_type TEXT,
                competition_level TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create site_plans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS site_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                site_type TEXT,
                core_feature TEXT,
                tech_stack TEXT,
                headline TEXT,
                structure TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create search_history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                engine TEXT,
                results_count INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_keywords_word ON keywords(word)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_search_history_keyword ON search_history(keyword)')

        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")

    def save_keyword(self, keyword: str, search_volume: Optional[int] = None,
                    trend_score: Optional[float] = None, intent_type: Optional[str] = None,
                    competition_level: Optional[str] = None) -> bool:
        """Save or update a keyword"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR REPLACE INTO keywords
                (word, search_volume, trend_score, intent_type, competition_level)
                VALUES (?, ?, ?, ?, ?)
            ''', (keyword, search_volume, trend_score, intent_type, competition_level))

            conn.commit()
            conn.close()
            logger.info(f"Saved keyword: {keyword}")
            return True
        except Exception as e:
            logger.error(f"Error saving keyword {keyword}: {e}")
            return False

    def get_keywords(self, limit: int = 100) -> List[Dict]:
        """Retrieve keywords from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM keywords ORDER BY created_at DESC LIMIT ?', (limit,))
            rows = cursor.fetchall()

            keywords = []
            for row in rows:
                keywords.append({
                    'id': row[0],
                    'word': row[1],
                    'search_volume': row[2],
                    'trend_score': row[3],
                    'intent_type': row[4],
                    'competition_level': row[5],
                    'created_at': row[6]
                })

            conn.close()
            return keywords
        except Exception as e:
            logger.error(f"Error retrieving keywords: {e}")
            return []

    def save_site_plan(self, keyword: str, site_type: str, core_feature: str,
                      tech_stack: str, headline: str, structure: str) -> bool:
        """Save a site plan"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO site_plans
                (keyword, site_type, core_feature, tech_stack, headline, structure)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (keyword, site_type, core_feature, tech_stack, headline, structure))

            conn.commit()
            conn.close()
            logger.info(f"Saved site plan for: {keyword}")
            return True
        except Exception as e:
            logger.error(f"Error saving site plan for {keyword}: {e}")
            return False

    def get_site_plans(self, keyword: Optional[str] = None) -> List[Dict]:
        """Retrieve site plans"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if keyword:
                cursor.execute('SELECT * FROM site_plans WHERE keyword = ?', (keyword,))
            else:
                cursor.execute('SELECT * FROM site_plans ORDER BY created_at DESC')

            rows = cursor.fetchall()

            plans = []
            for row in rows:
                plans.append({
                    'id': row[0],
                    'keyword': row[1],
                    'site_type': row[2],
                    'core_feature': row[3],
                    'tech_stack': row[4],
                    'headline': row[5],
                    'structure': row[6],
                    'created_at': row[7]
                })

            conn.close()
            return plans
        except Exception as e:
            logger.error(f"Error retrieving site plans: {e}")
            return []

    def log_search(self, keyword: str, engine: str, results_count: int) -> bool:
        """Log a search operation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO search_history (keyword, engine, results_count)
                VALUES (?, ?, ?)
            ''', (keyword, engine, results_count))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error logging search: {e}")
            return False

    def get_search_history(self, limit: int = 100) -> List[Dict]:
        """Retrieve search history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM search_history
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))

            rows = cursor.fetchall()

            history = []
            for row in rows:
                history.append({
                    'id': row[0],
                    'keyword': row[1],
                    'engine': row[2],
                    'results_count': row[3],
                    'timestamp': row[4]
                })

            conn.close()
            return history
        except Exception as e:
            logger.error(f"Error retrieving search history: {e}")
            return []

    def clear_all_data(self) -> bool:
        """Clear all data from tables (for testing)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM keywords')
            cursor.execute('DELETE FROM site_plans')
            cursor.execute('DELETE FROM search_history')

            conn.commit()
            conn.close()
            logger.info("All data cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing data: {e}")
            return False
