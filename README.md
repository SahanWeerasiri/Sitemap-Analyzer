# 🔍 Sitemap Analyzer

A powerful, intelligent Python backend service designed for comprehensive website analysis through sitemap parsing and web crawling. This tool automatically discovers and analyzes website sitemaps, identifies technical SEO issues, detects broken links, and finds orphaned pages to help maintain optimal website health and search engine visibility.

## 🚀 Overview

The Sitemap Analyzer is built for web developers, SEO professionals, and digital marketers who need to ensure their websites are properly structured and accessible. It goes beyond simple sitemap parsing by intelligently discovering sitemaps through multiple methods and providing actionable insights about website issues.

**What makes this analyzer special:**
- **Zero Configuration**: Just provide any website URL - the analyzer handles the rest
- **Intelligent Discovery**: Automatically finds sitemaps even when they're not obvious
- **Comprehensive Analysis**: Checks for broken links, SEO issues, and orphaned content
- **Robust Fallbacks**: Works even when websites don't have traditional sitemaps
- **Production Ready**: Built with enterprise-level logging, error handling, and scalability

## 🎯 Key Features

### Core Analysis Capabilities
*   **🔗 Broken Link Detection**: Identifies and reports HTTP 4xx/5xx errors, connection failures, and inaccessible URLs
*   **🏝️ Orphan Page Detection**: Discovers pages listed in sitemaps but not linked internally, indicating potential navigation issues
*   **📊 SEO Analysis**: Detects missing meta descriptions, analyzes title tags, and identifies other on-page SEO problems
*   **📈 Performance Monitoring**: Tracks analysis duration and provides detailed timing metrics

### Advanced Discovery Engine
*   **🤖 Intelligent Sitemap Discovery**: Automatically locates sitemaps using multiple strategies without manual intervention
*   **📑 Sitemap Index Support**: Seamlessly handles complex sitemap structures with multiple index files
*   **🔄 Robots.txt Fallback**: Uses robots.txt as an analysis source when traditional sitemaps aren't available
*   **🎯 Flexible URL Input**: Accepts any website URL format - domain, subdirectory, or direct file paths

### Technical Excellence
*   **⚡ Concurrent Processing**: Utilizes thread pools for fast, parallel analysis of multiple URLs
*   **📝 Comprehensive Logging**: Multi-level logging system for debugging, monitoring, and audit trails
*   **🛡️ Error Resilience**: Graceful handling of network failures, malformed content, and edge cases
*   **📊 Multiple Output Formats**: Generates reports in JSON, CSV, and other structured formats

## 🔍 Sitemap Discovery System

The analyzer employs a sophisticated multi-tier discovery system that ensures comprehensive website analysis regardless of how the sitemap is configured.

The analyzer intelligently discovers sitemaps using multiple strategies:

### 🎯 Supported Input Formats

The analyzer accepts virtually any website-related URL and intelligently determines the best analysis approach:

1. **📄 Direct Sitemap URLs**: `https://example.com/sitemap.xml`
   - Immediately validates and processes XML sitemap files
   - Supports both regular sitemaps and sitemap index files

2. **🌐 Domain URLs**: `https://example.com` or `https://example.com/`
   - Performs comprehensive discovery starting from the domain root
   - Checks robots.txt, common locations, and server configurations

3. **🤖 Robots.txt URLs**: `https://example.com/robots.txt`
   - Parses robots.txt for sitemap declarations and crawl directives
   - Extracts URLs from Allow/Disallow rules when no sitemap exists

4. **📁 Any Website Path**: `https://example.com/products/category`
   - Extracts the base domain and applies full discovery logic
   - Useful for analyzing specific site sections or deep-linked pages

### 🔄 Multi-Tier Discovery Process

The analyzer employs a systematic approach to ensure no sitemap goes undiscovered:

**Tier 1: Direct Validation**
- If the provided URL ends with `.xml`, validates it as a sitemap
- Checks content-type headers and XML structure validity
- Immediately proceeds to analysis if valid

**Tier 2: Robots.txt Intelligence**
- Fetches and parses the website's robots.txt file
- Searches for `Sitemap:` declarations and validates each reference
- Extracts crawl rules that can indicate important pages

**Tier 3: Common Location Scanning**
- Systematically checks standard sitemap locations:
  - `/sitemap.xml` - Most common location
  - `/sitemap_index.xml` - Index files for large sites
  - `/sitemaps.xml` - Alternative naming convention
  - `/sitemap1.xml` - Numbered sitemap files

**Tier 4: Robots.txt Fallback Analysis**
- When no traditional sitemap exists, uses robots.txt as a URL source
- Analyzes Allow/Disallow directives to identify important pages
- Adds common website sections (/, /about, /contact, etc.) as baseline URLs

### 🗂️ Advanced Sitemap Index Support

Modern websites often use sitemap index files to organize large amounts of content. The analyzer seamlessly handles these complex structures:

- **🔍 Automatic Detection**: Identifies `<sitemapindex>` root elements in XML files
- **📥 Recursive Fetching**: Downloads and parses all individual sitemaps referenced in the index
- **🔗 URL Aggregation**: Combines URLs from multiple sitemaps into a unified analysis dataset
- **⚡ Parallel Processing**: Fetches multiple sitemap files concurrently for optimal performance
- **🛡️ Error Tolerance**: Continues analysis even if some individual sitemaps are inaccessible

### 🤖 Intelligent Robots.txt Fallback

When traditional sitemaps aren't available, the analyzer transforms robots.txt into a valuable analysis source:

**URL Extraction Strategy:**
1. **📋 Directive Analysis**: Parses `Allow:` and `Disallow:` rules to identify significant pages
2. **🔗 Sitemap References**: Processes any `Sitemap:` declarations found in robots.txt
3. **🎯 Smart Filtering**: Excludes wildcard patterns and focuses on specific, crawlable paths
4. **🏠 Common Pages**: Adds standard website sections when specific URLs aren't found

#### 📝 Example Robots.txt Analysis

```robotstxt
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /public/blog/
Allow: /api/documentation
Disallow: /temp/*

Sitemap: https://example.com/sitemap.xml
Sitemap: https://example.com/news-sitemap.xml
```

**Extracted Analysis Targets:**
- ✅ `https://example.com/public/blog/` (from Allow directive)
- ✅ `https://example.com/api/documentation` (from Allow directive)  
- ✅ URLs from `sitemap.xml` and `news-sitemap.xml` (from Sitemap declarations)
- ✅ Common fallback pages: `/`, `/about`, `/contact` (if no specific URLs found)

### 💡 Usage Examples & Real-World Scenarios

### 💡 Usage Examples & Real-World Scenarios

```python
from src.sitemap_analyzer import SitemapAnalyzer

# Scenario 1: E-commerce Site Analysis
analyzer = SitemapAnalyzer("https://mystore.com")
results = analyzer.analyze()
# Automatically finds product catalog sitemaps, checks for broken product links

# Scenario 2: News Website with Multiple Sitemaps  
analyzer = SitemapAnalyzer("https://newssite.com/sitemap_index.xml")
results = analyzer.analyze()
# Processes news, articles, and category sitemaps from the index

# Scenario 3: Corporate Website without Sitemap
analyzer = SitemapAnalyzer("https://company.com")
results = analyzer.analyze()
# Falls back to robots.txt analysis, finds key corporate pages

# Scenario 4: Blog Subdirectory Analysis
analyzer = SitemapAnalyzer("https://website.com/blog/")
results = analyzer.analyze()
# Discovers blog-specific sitemap or analyzes blog structure

# The analyzer provides consistent logging throughout:
# INFO - Attempting to find sitemap URL from: https://mystore.com
# INFO - Checking robots.txt at: https://mystore.com/robots.txt  
# INFO - Found sitemap URL in robots.txt: https://mystore.com/product-sitemap.xml
# INFO - Detected regular sitemap file
# INFO - Found 1,247 URLs in total from sitemap(s)
```

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.7+** (Recommended: Python 3.9+)
- **pip** package manager
- **Internet connection** for analyzing remote websites

### Quick Start Installation

### Quick Start Installation

```bash
# 1. Clone the repository
git clone https://github.com/SahanWeerasiri/Sitemap-Analyzer.git
cd Sitemap-Analyzer

# 2. Create and activate virtual environment
python -m venv venv

# On Windows:
.\venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run your first analysis
python main.py
```

### 🔧 Dependencies

The analyzer uses carefully selected, lightweight dependencies:

```
requests>=2.28.0       # HTTP client for robust web requests
beautifulsoup4>=4.11.0 # HTML/XML parsing with excellent error handling  
python-dotenv>=0.19.0  # Environment variable management
```

## 🚀 Usage Guide

### Command Line Interface

The simplest way to get started is through the command line:

```bash
# Analyze any website - the tool handles sitemap discovery automatically
python main.py

# Set a specific website through environment variable
export SITEMAP_URL="https://your-website.com"
python main.py

# Or modify main.py to set your target URL directly
```

### 📊 Programmatic Usage

For integration into larger applications or custom analysis workflows:

### 📊 Programmatic Usage

For integration into larger applications or custom analysis workflows:

```python
import logging
from src.sitemap_analyzer import SitemapAnalyzer

# Configure logging level for your needs
analyzer = SitemapAnalyzer("https://your-website.com")
analyzer.set_log_level(logging.INFO)  # DEBUG, INFO, WARNING, ERROR

# Run comprehensive analysis
results = analyzer.analyze()

# Access specific results
print(f"Found {len(results['broken_links'])} broken links")
print(f"Found {len(results['orphan_pages'])} orphan pages")  
print(f"Found {len(results['seo_issues'])} SEO issues")

# Handle errors gracefully
if "error" in results:
    print(f"Analysis failed: {results['error']}")
else:
    # Process successful results
    for broken_link in results['broken_links']:
        print(f"Broken: {broken_link['url']} (Status: {broken_link['status_code']})")
```

### 🎛️ Advanced Configuration

#### Environment Variables

Create a `.env` file in the project root for customization:

```env
# Target website for analysis
SITEMAP_URL=https://your-website.com

# Analysis parameters  
CRAWL_DEPTH=3           # How deep to crawl for internal links
TIMEOUT=10              # Request timeout in seconds
MAX_WORKERS=10          # Concurrent thread pool size

# API Configuration (if using API mode)
PORT=8000              # Server port
DEBUG=False            # Debug mode
```

#### Logging Configuration

The analyzer supports multiple logging configurations:

```python
import logging
from src.sitemap_analyzer import SitemapAnalyzer

# Method 1: Simple level setting
analyzer = SitemapAnalyzer("https://example.com")
analyzer.set_log_level(logging.DEBUG)  # Verbose output

# Method 2: Custom logging configuration  
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('custom_analysis.log'),
        logging.StreamHandler()
    ]
)

# Method 3: Using the provided logging.conf file
import logging.config
logging.config.fileConfig('logging.conf')
```

## 📈 Understanding Analysis Results

The analyzer returns a comprehensive dictionary with three main categories of findings:

### 🔗 Broken Links Analysis
```python
{
    "broken_links": [
        {
            "url": "https://example.com/old-page",
            "status_code": 404
        },
        {
            "url": "https://example.com/server-error", 
            "status_code": 500
        },
        {
            "url": "https://example.com/timeout",
            "status_code": "Connection Error"
        }
    ]
}
```

### 🏝️ Orphan Pages Detection
```python
{
    "orphan_pages": [
        "https://example.com/forgotten-page",
        "https://example.com/unreachable-content",
        "https://example.com/isolated-article"
    ]
}
```

### 📊 SEO Issues Identification  
```python
{
    "seo_issues": [
        {
            "url": "https://example.com/no-description",
            "issue": "Missing meta description"
        },
        {
            "url": "https://example.com/fetch-error",
            "issue": "Error fetching page"
        }
    ]
}
```

## 🎯 Use Cases & Applications

### For Web Developers
- **Pre-deployment Checks**: Validate sitemaps before going live
- **Continuous Integration**: Integrate into CI/CD pipelines for automated testing
- **Migration Validation**: Ensure all URLs work correctly after site migrations
- **Performance Monitoring**: Regular checks for link rot and accessibility issues

### For SEO Professionals  
- **Technical SEO Audits**: Comprehensive analysis of crawlable content
- **Content Gap Analysis**: Identify orphaned pages that need better internal linking
- **Meta Tag Optimization**: Find pages missing crucial SEO elements
- **Sitemap Optimization**: Ensure search engines can discover all important content

### For Digital Marketers
- **Campaign URL Validation**: Verify landing pages are accessible before campaigns
- **Content Inventory**: Understand the full scope of published content
- **User Experience Audit**: Identify broken links that hurt user experience
- **Competitive Analysis**: Analyze competitor sitemap structures (public sitemaps only)

## 🔧 API Integration (Future Enhancement)

While currently CLI-focused, the architecture supports future API development:

```python
# Planned API endpoints:
# POST /api/analyze
# GET /api/status/{job_id}  
# GET /api/results/{job_id}
```

### CLI Mode (Current)

### CLI Mode (Current)

Run immediate analysis from the command line:

```bash
# Basic analysis with default settings
python main.py

# With custom logging level  
python -c "
import logging
from src.sitemap_analyzer import SitemapAnalyzer
analyzer = SitemapAnalyzer('https://example.com')
analyzer.set_log_level(logging.DEBUG)
results = analyzer.analyze()
print(f'Analysis complete: {len(results.get(\"broken_links\", []))} issues found')
"
```

## ⚙️ Configuration Reference

## ⚙️ Configuration Reference

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SITEMAP_URL` | `https://smallpdf.com/` | Target website or sitemap URL for analysis |
| `CRAWL_DEPTH` | `3` | Maximum depth for recursive crawling (future feature) |
| `TIMEOUT` | `10` | HTTP request timeout in seconds |
| `MAX_WORKERS` | `10` | Number of concurrent threads for parallel processing |
| `LOG_LEVEL` | `INFO` | Logging verbosity: DEBUG, INFO, WARNING, ERROR |

### Performance Tuning

```python
# For large websites, adjust these parameters:
analyzer = SitemapAnalyzer("https://large-site.com")

# Increase timeout for slow servers
analyzer.session.timeout = 30  

# Reduce concurrency for rate-limited sites
# (Modify MAX_WORKERS in analyze() method)
```

## 📊 Advanced Logging System

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

## 🧪 Testing & Examples

### Quick Test Scripts

The project includes several test scripts to demonstrate functionality:

```bash
# Test the enhanced URL discovery system
python test_url_discovery.py

# Test robots.txt fallback functionality  
python test_robots_fallback.py

# Demo different logging levels
python demo_logging.py

# Example of enhanced discovery features
python example_enhanced_discovery.py
```

### Sample Analysis Run

```bash
$ python main.py
2025-07-13 16:25:51 - INFO - Starting sitemap analysis for: https://smallpdf.com/
2025-07-13 16:25:51 - INFO - The analyzer will automatically:
2025-07-13 16:25:51 - INFO - 1. Check if the URL is a direct sitemap.xml
2025-07-13 16:25:51 - INFO - 2. Look for sitemap in robots.txt if not found  
2025-07-13 16:25:51 - INFO - 3. Try common sitemap locations
2025-07-13 16:25:52 - INFO - Found sitemap URL in robots.txt: https://smallpdf.com/sitemap.xml
2025-07-13 16:25:53 - INFO - Found 1,247 URLs in total from sitemap(s)
2025-07-13 16:26:15 - INFO - Analysis completed in 22.34 seconds

============================================================
SITEMAP ANALYSIS RESULTS
============================================================
Broken Links: 3
Orphan Pages: 12  
SEO Issues: 8

Detailed results saved to 'analysis_results.json'
```

## 🤝 Contributing

We welcome contributions to improve the Sitemap Analyzer! Here's how you can help:

### Development Setup

```bash
# Fork the repository and clone your fork
git clone https://github.com/yourusername/Sitemap-Analyzer.git
cd Sitemap-Analyzer

# Create a development branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Make your changes and test thoroughly
python test_url_discovery.py
python test_robots_fallback.py

# Commit and push your changes
git add .
git commit -m "Add: Description of your changes"
git push origin feature/your-feature-name
```

### Areas for Contribution

- **🔌 API Development**: Build REST API endpoints for web integration
- **📊 Additional Analysis Types**: New checks for accessibility, performance, etc.
- **🎨 Output Formats**: CSV, XML, PDF report generation
- **⚡ Performance Optimization**: Caching, request optimization, parallel processing improvements
- **🧪 Test Coverage**: Unit tests, integration tests, edge case handling
- **📚 Documentation**: Tutorials, use case examples, API documentation

## 🐛 Troubleshooting

### Common Issues & Solutions

**Issue: "AttributeError: 'SitemapAnalyzer' object has no attribute 'session'"**
```bash
# Solution: Ensure you're using the latest version where session initialization was fixed
git pull origin master
```

**Issue: "No URLs found in sitemap"**
```bash
# The website might not have a traditional sitemap
# The analyzer will automatically fall back to robots.txt analysis
# Check the logs to see what discovery method was used
```

**Issue: "Connection timeout errors"**
```python
# Increase timeout for slow websites
analyzer = SitemapAnalyzer("https://slow-website.com")
analyzer.session.timeout = 30  # Increase from default 10 seconds
```

**Issue: "Too many concurrent requests"**
```python
# Some websites rate-limit requests
# Reduce MAX_WORKERS in the analyze() method or implement delays
```

### Debug Mode

Enable debug logging for detailed troubleshooting:

```python
import logging
analyzer = SitemapAnalyzer("https://problem-site.com")
analyzer.set_log_level(logging.DEBUG)
results = analyzer.analyze()
```

## 📞 Support & Community

- **🐛 Bug Reports**: [GitHub Issues](https://github.com/SahanWeerasiri/Sitemap-Analyzer/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/SahanWeerasiri/Sitemap-Analyzer/discussions)
- **📖 Documentation**: This README and inline code documentation
- **👨‍💻 Developer**: [@SahanWeerasiri](https://github.com/SahanWeerasiri)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **BeautifulSoup4** for robust HTML/XML parsing
- **Requests** library for reliable HTTP client functionality
- **Python community** for excellent ecosystem and documentation
- **SEO community** for insights into technical SEO requirements

---

**Built with ❤️ for web developers, SEO professionals, and anyone who cares about website quality.**