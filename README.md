# Sitemap Analyzer

A backend service (Python) for analyzing website sitemaps, identifying broken links, orphan pages, and potential SEO issues. Provides both API and CLI interfaces with intelligent sitemap discovery.

## Key Features

*   **Broken Link Detection:** Identifies and reports broken links within the sitemap.
*   **Orphan Page Detection:** Detects pages not linked to from within the sitemap.
*   **SEO Analysis:** Provides insights into potential SEO issues (e.g., missing titles, descriptions).
*   **Intelligent Sitemap Discovery:** Automatically finds sitemaps from robots.txt or common locations.
*   **Sitemap Index Support:** Handles sitemap index files containing multiple sitemaps.
*   **Flexible URL Input:** Accepts domain URLs, robots.txt URLs, or direct sitemap URLs.
*   **Customizable Crawl Depth:** Configure how deep the analyzer crawls the website.
*   **Detailed Reporting:** Generates comprehensive reports in various formats (e.g., JSON, CSV).
*   **Comprehensive Logging:** Track analysis progress with detailed logging at multiple levels.

## Sitemap Discovery

The analyzer intelligently discovers sitemaps using multiple strategies:

### Supported URL Formats

1. **Direct Sitemap URL**: `https://example.com/sitemap.xml`
   - Uses the URL directly if it's a valid sitemap

2. **Domain URL**: `https://example.com` or `https://example.com/`
   - Checks robots.txt for sitemap declarations
   - Falls back to common sitemap locations

3. **Robots.txt URL**: `https://example.com/robots.txt`
   - Parses robots.txt to find sitemap references

4. **Any Domain Path**: `https://example.com/some/path`
   - Extracts base domain and applies discovery logic

### Discovery Process

1. **Direct Check**: If URL ends with `.xml`, verify it's a valid sitemap
2. **Robots.txt Parsing**: Look for `Sitemap:` declarations in robots.txt
3. **Common Locations**: Try standard sitemap paths:
   - `/sitemap.xml`
   - `/sitemap_index.xml`
   - `/sitemaps.xml`
   - `/sitemap1.xml`
4. **Robots.txt Fallback**: If no sitemap found, use robots.txt for URL extraction

### Sitemap Index Support

The analyzer automatically detects and handles sitemap index files:
- Identifies `<sitemapindex>` root elements
- Fetches all individual sitemaps referenced in the index
- Combines URLs from all sitemaps for comprehensive analysis

### Robots.txt Fallback

When no sitemap.xml is found, the analyzer automatically falls back to using robots.txt:

1. **URL Extraction from robots.txt**: Analyzes `Allow:` and `Disallow:` directives to extract URLs
2. **Sitemap References**: Processes any `Sitemap:` declarations found in robots.txt
3. **Common Pages Fallback**: If no specific URLs are found, adds common pages (/, /about, /contact, etc.)

#### Example robots.txt Analysis

```
User-agent: *
Disallow: /admin/
Allow: /public/
Allow: /api/docs
Sitemap: https://example.com/sitemap.xml
```

From this robots.txt, the analyzer extracts:
- `/public/` → `https://example.com/public/`
- `/api/docs` → `https://example.com/api/docs`
- Attempts to fetch and parse `https://example.com/sitemap.xml`

### Usage Examples

```python
from src.sitemap_analyzer import SitemapAnalyzer

# All of these will work and automatically find the sitemap:
analyzer1 = SitemapAnalyzer("https://example.com")
analyzer2 = SitemapAnalyzer("https://example.com/robots.txt")
analyzer3 = SitemapAnalyzer("https://example.com/sitemap.xml")
analyzer4 = SitemapAnalyzer("https://example.com/some/page")

# The analyzer will log its discovery process:
# INFO - Attempting to find sitemap URL from: https://example.com
# INFO - Checking robots.txt at: https://example.com/robots.txt
# INFO - Found sitemap URL in robots.txt: https://example.com/sitemap.xml
```

## Setup

1.  Clone the repository: `git clone [repository_url]`
2.  Navigate to the project directory: `cd [project_directory]`
3.  Create a virtual environment: `python3 -m venv venv`
4.  Activate the virtual environment:
    *   Linux/macOS: `source venv/bin/activate`
    *   Windows: `.\venv\Scripts\activate`
5.  Install dependencies: `pip install -r requirements.txt`

## Usage

### API

1.  Run the application: `python main.py --mode api`
2.  The API will be available at `http://localhost:8000` (or configured address).

#### Endpoints

*   `POST /analyze`: Analyzes a sitemap.
    *   Request body: `{"sitemap_url": "URL_OF_SITEMAP"}`
    *   Response: `{"status": "success", "report": {...}}`  (or `{"status": "error", "message": "error details"}`)

### CLI

1.  Run the application: `python main.py --mode cli`

#### Commands

*   `analyze --sitemap_url URL_OF_SITEMAP --output_format [json|csv] --output_file OUTPUT_FILE`
    *   Analyzes the specified sitemap and saves the report to the specified file.

## Configuration

The application can be configured using environment variables:

*   `PORT`: The port the API server listens on (default: 8000).
*   `CRAWL_DEPTH`: The maximum crawl depth (default: 3).
*   `TIMEOUT`: Request timeout in seconds (default: 10).
*   `SITEMAP_URL`: Default sitemap URL to analyze.

## Logging

The Sitemap Analyzer includes comprehensive logging capabilities to help track the analysis process and debug issues:

### Logging Levels

*   **DEBUG**: Detailed information about each page crawl, link check, and SEO analysis
*   **INFO**: General progress information, summary statistics, and completion status
*   **WARNING**: Issues found such as broken links, SEO problems, crawling errors
*   **ERROR**: Critical errors that prevent analysis from completing

### Logging Configuration

#### Basic Usage
```python
from src.sitemap_analyzer import SitemapAnalyzer
import logging

# Create analyzer
analyzer = SitemapAnalyzer("https://example.com/sitemap.xml")

# Set logging level
analyzer.set_log_level(logging.DEBUG)  # For detailed debugging
analyzer.set_log_level(logging.INFO)   # For general information (default)
analyzer.set_log_level(logging.WARNING)  # For warnings and errors only
```

#### Log Files
By default, logs are written to:
- Console output (INFO level and above)
- `sitemap_analysis.log` file (all levels)
- `analysis_results.json` (detailed analysis results)

#### Using Configuration File
You can use the provided `logging.conf` file for advanced logging configuration:
```python
import logging.config
logging.config.fileConfig('logging.conf')
```

### Log Output Examples

**INFO Level:**
```
2025-07-13 10:30:15 - sitemap_analyzer - INFO - Initialized SitemapAnalyzer for https://example.com/sitemap.xml
2025-07-13 10:30:15 - sitemap_analyzer - INFO - Starting sitemap analysis
2025-07-13 10:30:16 - sitemap_analyzer - INFO - Found 150 URLs in sitemap
2025-07-13 10:30:25 - sitemap_analyzer - INFO - Analysis completed in 9.45 seconds
```

**DEBUG Level:**
```
2025-07-13 10:30:17 - sitemap_analyzer - DEBUG - Crawling page: https://example.com/about
2025-07-13 10:30:17 - sitemap_analyzer - DEBUG - Found 8 new internal links on https://example.com/about
2025-07-13 10:30:18 - sitemap_analyzer - DEBUG - Link OK: https://example.com/contact (Status: 200)
```

**WARNING Level:**
```
2025-07-13 10:30:20 - sitemap_analyzer - WARNING - Broken link detected: https://example.com/old-page (Status: 404)
2025-07-13 10:30:22 - sitemap_analyzer - WARNING - SEO issue detected: Missing meta description for https://example.com/products
```

## Example

```bash
python main.py --mode cli analyze --sitemap_url https://example.com/sitemap.xml --output_format json --output_file report.json
```

## License

[Specify the License used, e.g., MIT License]