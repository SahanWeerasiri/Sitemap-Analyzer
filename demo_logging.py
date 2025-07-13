#!/usr/bin/env python3
"""
Example script demonstrating the SitemapAnalyzer with different logging levels.
"""

import logging
from src.sitemap_analyzer import SitemapAnalyzer

def demo_with_debug_logging():
    """Demonstrate analyzer with debug logging enabled."""
    print("=== Running analysis with DEBUG logging ===")
    
    analyzer = SitemapAnalyzer("https://httpbin.org/robots.txt")  # Simple test URL
    analyzer.set_log_level(logging.DEBUG)
    
    # For demo purposes, let's just check the initialization
    print(f"Analyzer initialized for: {analyzer.sitemap_url}")
    print(f"Base URL: {analyzer.base_url}")

def demo_with_info_logging():
    """Demonstrate analyzer with info logging (default)."""
    print("\n=== Running analysis with INFO logging ===")
    
    analyzer = SitemapAnalyzer("https://httpbin.org/robots.txt")
    # INFO is default, no need to set
    
    print(f"Analyzer initialized for: {analyzer.sitemap_url}")
    print(f"Base URL: {analyzer.base_url}")

def demo_with_warning_logging():
    """Demonstrate analyzer with warning logging only."""
    print("\n=== Running analysis with WARNING logging ===")
    
    analyzer = SitemapAnalyzer("https://httpbin.org/robots.txt")
    analyzer.set_log_level(logging.WARNING)
    
    print(f"Analyzer initialized for: {analyzer.sitemap_url}")
    print(f"Base URL: {analyzer.base_url}")

if __name__ == "__main__":
    print("SitemapAnalyzer Logging Demo")
    print("=" * 40)
    
    demo_with_debug_logging()
    demo_with_info_logging()
    demo_with_warning_logging()
    
    print("\n=== Demo completed ===")
    print("The analyzer now includes comprehensive logging at different levels:")
    print("- DEBUG: Detailed information about each page crawl and check")
    print("- INFO: General progress information and summary statistics")
    print("- WARNING: Issues found (broken links, SEO problems, etc.)")
    print("- ERROR: Critical errors that prevent analysis")
