import os
import logging
import json
from dotenv import load_dotenv
from src.sitemap_analyzer import SitemapAnalyzer

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('sitemap_analysis.log')
        ]
    )

load_dotenv()

if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Get URL from environment or use default
    # Now supports: full sitemap URLs, domain URLs, or robots.txt URLs
    url = os.getenv("SITEMAP_URL", "https://smallpdf.com/")
    
    logger.info(f"Starting sitemap analysis for: {url}")
    logger.info("The analyzer will automatically:")
    logger.info("1. Check if the URL is a direct sitemap.xml")
    logger.info("2. Look for sitemap in robots.txt if not found")
    logger.info("3. Try common sitemap locations (/sitemap.xml, /sitemap_index.xml, etc.)")
    
    analyzer = SitemapAnalyzer(url)
    try:
        results = analyzer.analyze()
        
        # Pretty print the results
        print("\n" + "="*60)
        print("SITEMAP ANALYSIS RESULTS")
        print("="*60)
        
        if "error" in results:
            print(f"ERROR: {results['error']}")
            logger.error(f"Analysis failed: {results['error']}")
        else:
            print(f"Broken Links: {len(results['broken_links'])}")
            print(f"Orphan Pages: {len(results['orphan_pages'])}")
            print(f"SEO Issues: {len(results['seo_issues'])}")
            
            # Save detailed results to file
            with open('analysis_results.json', 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info("Analysis completed successfully")
            print("\nDetailed results saved to 'analysis_results.json'")
            
    except Exception as e:
        logger.error(f"An error occurred during analysis: {e}")
        print(f"An error occurred: {e}")
        raise