#!/usr/bin/env python3
"""
Test script demonstrating the enhanced SitemapAnalyzer that can work with
various URL formats including robots.txt, domain URLs, and sitemap URLs.
"""

import logging
from src.sitemap_analyzer import SitemapAnalyzer

def test_different_url_formats():
    """Test the analyzer with different URL formats."""
    
    # Set up basic logging
    logging.basicConfig(level=logging.INFO)
    
    test_cases = [
        {
            "name": "Direct sitemap URL",
            "url": "https://example.com/sitemap.xml",
            "description": "Should use the URL directly if it's a valid sitemap"
        },
        {
            "name": "Domain URL", 
            "url": "https://example.com",
            "description": "Should check robots.txt and common sitemap locations"
        },
        {
            "name": "Robots.txt URL",
            "url": "https://example.com/robots.txt", 
            "description": "Should parse robots.txt to find sitemap references"
        },
        {
            "name": "Domain with path",
            "url": "https://example.com/some/path",
            "description": "Should extract base domain and find sitemap"
        }
    ]
    
    print("Testing SitemapAnalyzer URL Discovery")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"URL: {test_case['url']}")
        print(f"Expected: {test_case['description']}")
        print("-" * 30)
        
        try:
            # Just test initialization to see URL discovery
            analyzer = SitemapAnalyzer(test_case['url'])
            print(f"✓ Resolved sitemap URL: {analyzer.sitemap_url}")
            print(f"✓ Base URL: {analyzer.base_url}")
            
        except Exception as e:
            print(f"✗ Error: {e}")

def demonstrate_sitemap_index_handling():
    """Demonstrate handling of sitemap index files."""
    print("\n" + "=" * 50)
    print("Sitemap Index Handling Demo")
    print("=" * 50)
    
    print("The analyzer now supports:")
    print("• Regular sitemap.xml files")
    print("• Sitemap index files (containing multiple sitemaps)")
    print("• Automatic discovery via robots.txt")
    print("• Common sitemap locations fallback")
    print()
    print("When a sitemap index is detected, the analyzer will:")
    print("1. Parse the index to find individual sitemap URLs")
    print("2. Fetch each individual sitemap")
    print("3. Combine all URLs for comprehensive analysis")

if __name__ == "__main__":
    test_different_url_formats()
    demonstrate_sitemap_index_handling()
    
    print("\n" + "=" * 50)
    print("Summary of Enhancements")
    print("=" * 50)
    print("✓ Automatic sitemap discovery from robots.txt")
    print("✓ Common sitemap location fallback")
    print("✓ Sitemap index file support")
    print("✓ Flexible URL input (domain, robots.txt, sitemap.xml)")
    print("✓ Comprehensive logging of discovery process")
    print("✓ Error handling for invalid/missing sitemaps")
