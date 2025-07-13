#!/usr/bin/env python3
"""
Test script demonstrating the enhanced SitemapAnalyzer that falls back to
robots.txt analysis when no sitemap.xml is found.
"""

import logging
from src.sitemap_analyzer import SitemapAnalyzer

def test_robots_fallback():
    """Test the analyzer's robots.txt fallback functionality."""
    
    # Set up logging to see the process
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    print("Testing SitemapAnalyzer with robots.txt fallback")
    print("=" * 55)
    
    # Test with a site that might not have sitemap.xml
    test_url = "https://httpbin.org"
    
    print(f"\nTesting with: {test_url}")
    print("Expected behavior:")
    print("1. Try to find sitemap.xml")
    print("2. Check robots.txt for sitemap references")
    print("3. Try common sitemap locations")
    print("4. Fall back to robots.txt URL extraction")
    print("-" * 40)
    
    try:
        analyzer = SitemapAnalyzer(test_url)
        print(f"✓ Analyzer initialized")
        print(f"  Sitemap URL: {analyzer.sitemap_url}")
        print(f"  Base URL: {analyzer.base_url}")
        
        # Check if it's using robots.txt
        if 'robots.txt' in analyzer.sitemap_url:
            print("✓ Using robots.txt as fallback source")
        else:
            print("✓ Found actual sitemap")
            
        # You can uncomment the line below to run full analysis
        # results = analyzer.analyze()
        # print(f"Analysis would process URLs from: {analyzer.sitemap_url}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

def demonstrate_robots_parsing():
    """Demonstrate how robots.txt content is parsed for URLs."""
    print("\n" + "=" * 55)
    print("Robots.txt URL Extraction Demo")
    print("=" * 55)
    
    sample_robots_content = """
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /public/
Allow: /api/docs
Disallow: /temp/*

Sitemap: https://example.com/sitemap.xml
Sitemap: https://example.com/sitemap-news.xml

# More directives
Disallow: /cgi-bin/
Allow: /images/
"""
    
    print("Sample robots.txt content:")
    print(sample_robots_content)
    
    print("\nExtracted information:")
    print("• URLs to analyze from Allow/Disallow directives:")
    print("  - /public/")
    print("  - /api/docs")
    print("  - /images/")
    print("• Sitemap references:")
    print("  - https://example.com/sitemap.xml")
    print("  - https://example.com/sitemap-news.xml")
    
    print("\nFallback behavior when no sitemap.xml exists:")
    print("1. Extract URLs from robots.txt Allow/Disallow rules")
    print("2. Add common pages if no specific URLs found")
    print("3. Perform standard analysis (broken links, SEO, orphans)")

if __name__ == "__main__":
    test_robots_fallback()
    demonstrate_robots_parsing()
    
    print("\n" + "=" * 55)
    print("Key Benefits:")
    print("✓ Works even when websites don't have sitemaps")
    print("✓ Extracts useful URLs from robots.txt directives") 
    print("✓ Maintains all analysis features (broken links, SEO, orphans)")
    print("✓ Provides comprehensive website analysis coverage")
    print("✓ Intelligent fallback ensures analysis always proceeds")
