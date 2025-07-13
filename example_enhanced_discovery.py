#!/usr/bin/env python3
"""
Simple example demonstrating the enhanced SitemapAnalyzer
with automatic sitemap discovery capabilities.
"""

from src.sitemap_analyzer import SitemapAnalyzer
import logging

# Set up logging to see the discovery process
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    print("SitemapAnalyzer Enhanced URL Discovery Demo")
    print("=" * 50)
    
    # Example 1: Using just a domain name
    print("\n1. Analyzing with domain URL only:")
    print("   Input: https://httpbin.org")
    print("   Expected: Will check robots.txt and common locations")
    
    try:
        analyzer = SitemapAnalyzer("https://httpbin.org")
        print(f"   ✓ Discovered sitemap: {analyzer.sitemap_url}")
    except Exception as e:
        print(f"   ✗ Could not find sitemap: {e}")
    
    # Example 2: Using a robots.txt URL
    print("\n2. Analyzing with robots.txt URL:")
    print("   Input: https://httpbin.org/robots.txt")
    print("   Expected: Will parse robots.txt for sitemap references")
    
    try:
        analyzer = SitemapAnalyzer("https://httpbin.org/robots.txt")
        print(f"   ✓ Discovered sitemap: {analyzer.sitemap_url}")
    except Exception as e:
        print(f"   ✗ Could not find sitemap: {e}")
    
    # Example 3: Direct sitemap URL
    print("\n3. Analyzing with direct sitemap URL:")
    print("   Input: https://example.com/sitemap.xml")
    print("   Expected: Will use URL directly if valid")
    
    try:
        analyzer = SitemapAnalyzer("https://example.com/sitemap.xml")
        print(f"   ✓ Sitemap URL: {analyzer.sitemap_url}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("Key Benefits of Enhanced Discovery:")
    print("• No need to manually find sitemap URLs")
    print("• Handles sitemap index files automatically")
    print("• Works with any domain or website URL")
    print("• Comprehensive logging shows discovery process")
    print("• Graceful fallback to common sitemap locations")
    
    print("\nTo run a full analysis, use:")
    print("analyzer = SitemapAnalyzer('https://your-domain.com')")
    print("results = analyzer.analyze()")

if __name__ == "__main__":
    main()
