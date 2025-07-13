import os
from dotenv import load_dotenv
from src.sitemap_analyzer import SitemapAnalyzer

load_dotenv()

# Example Usage (Adjust as needed)
if __name__ == "__main__":
    sitemap_url = "https://example.com/sitemap.xml"  # Replace with the actual sitemap URL
    analyzer = SitemapAnalyzer(sitemap_url)
    results = analyzer.analyze()
    print(results)