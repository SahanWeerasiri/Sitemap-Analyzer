import os
from dotenv import load_dotenv
from src.sitemap_analyzer import SitemapAnalyzer

load_dotenv()

if __name__ == "__main__":
    sitemap_url = os.getenv("SITEMAP_URL", "https://example.com/sitemap.xml")
    analyzer = SitemapAnalyzer(sitemap_url)
    try:
        results = analyzer.analyze()
        for result in results:
            print(result)
    except Exception as e:
        print(f"An error occurred: {e}")