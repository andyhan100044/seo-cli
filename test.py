#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO CLI - Test Script
Simple test to verify core functionality
"""

import sys
import os

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")

    try:
        from db import Database
        print("[OK] Database module imported successfully")
    except Exception as e:
        print(f"[FAIL] Database module import failed: {e}")
        return False

    try:
        from skills.hot import collect_hot_words
        print("[OK] Hot words module imported successfully")
    except Exception as e:
        print(f"[FAIL] Hot words module import failed: {e}")
        return False

    try:
        from skills.trend import verify_trends
        print("[OK] Trends module imported successfully")
    except Exception as e:
        print(f"[FAIL] Trends module import failed: {e}")
        return False

    try:
        from skills.intent import analyze_intent
        print("[OK] Intent module imported successfully")
    except Exception as e:
        print(f"[FAIL] Intent module import failed: {e}")
        return False

    try:
        from skills.outline import generate_outline
        print("[OK] Outline module imported successfully")
    except Exception as e:
        print(f"[FAIL] Outline module import failed: {e}")
        return False

    try:
        from external.searxng import SearXNGClient
        print("[OK] SearXNG client imported successfully")
    except Exception as e:
        print(f"[FAIL] SearXNG client import failed: {e}")
        return False

    try:
        from external.trends import TrendsClient
        print("[OK] Trends client imported successfully")
    except Exception as e:
        print(f"[FAIL] Trends client import failed: {e}")
        return False

    return True

def test_database():
    """Test database initialization"""
    print("\nTesting database...")

    try:
        from db import Database
        db = Database(db_path="./test_seo_cli.db")

        # Test saving a keyword
        success = db.save_keyword("test keyword", search_volume=1000, trend_score=75.5)
        if success:
            print("[OK] Database save operation successful")
        else:
            print("[FAIL] Database save operation failed")
            return False

        # Test retrieving keywords
        keywords = db.get_keywords(limit=10)
        if keywords:
            print(f"[OK] Database retrieve operation successful ({len(keywords)} keywords)")
        else:
            print("[FAIL] Database retrieve operation failed")
            return False

        # Clean up test database
        if os.path.exists("./test_seo_cli.db"):
            os.remove("./test_seo_cli.db")
            print("[OK] Test database cleaned up")

        return True

    except Exception as e:
        print(f"[FAIL] Database test failed: {e}")
        return False

def test_intent_analysis():
    """Test intent analysis functionality"""
    print("\nTesting intent analysis...")

    try:
        from skills.intent import analyze_intent

        # Test transactional intent
        result = analyze_intent("buy AI generator", longtail_count=5)
        if result['intent'] == 'transactional':
            print("[OK] Transactional intent detection successful")
        else:
            print(f"[FAIL] Transactional intent detection failed: {result['intent']}")
            return False

        # Test informational intent
        result = analyze_intent("what is AI", longtail_count=5)
        if result['intent'] == 'informational':
            print("[OK] Informational intent detection successful")
        else:
            print(f"[FAIL] Informational intent detection failed: {result['intent']}")
            return False

        # Test longtail generation
        if len(result['longtail_words']) == 5:
            print("[OK] Longtail generation successful")
        else:
            print(f"[FAIL] Longtail generation failed: {len(result['longtail_words'])} words")
            return False

        # Test site plan generation
        if 'site_plan' in result and result['site_plan']['type']:
            print("[OK] Site plan generation successful")
        else:
            print("[FAIL] Site plan generation failed")
            return False

        return True

    except Exception as e:
        print(f"[FAIL] Intent analysis test failed: {e}")
        return False

def test_outline_generation():
    """Test outline generation functionality"""
    print("\nTesting outline generation...")

    try:
        from skills.outline import generate_tool_outline, estimate_word_count

        # Test tool outline generation
        outline = generate_tool_outline("test tool")
        if outline['H1'] == 'test tool在线工具':
            print("[OK] Tool outline generation successful")
        else:
            print(f"[FAIL] Tool outline generation failed: {outline['H1']}")
            return False

        # Test word count estimation
        word_count = estimate_word_count(outline)
        if word_count > 0:
            print(f"[OK] Word count estimation successful ({word_count} words)")
        else:
            print("[FAIL] Word count estimation failed")
            return False

        return True

    except Exception as e:
        print(f"[FAIL] Outline generation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("SEO CLI - Test Suite")
    print("=" * 60)

    all_passed = True

    # Test imports
    if not test_imports():
        all_passed = False

    # Test database
    if not test_database():
        all_passed = False

    # Test intent analysis
    if not test_intent_analysis():
        all_passed = False

    # Test outline generation
    if not test_outline_generation():
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] All tests passed!")
        print("=" * 60)
        return 0
    else:
        print("[FAILED] Some tests failed!")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
