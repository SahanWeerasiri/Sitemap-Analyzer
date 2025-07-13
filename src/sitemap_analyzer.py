import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import concurrent.futures
import logging
import time

class SitemapAnalyzer:
    def __init__(self, sitemap_url):
        """Initializes the SitemapAnalyzer with the sitemap URL."""
        # Set up logging
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        
        # Initialize session first (needed for sitemap discovery)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'SitemapAnalyzerBot/1.0'})
        self.visited = set()
        
        # Find the actual sitemap URL (handle robots.txt, common locations, etc.)
        self.sitemap_url = self._find_sitemap_url(sitemap_url)
        self.base_url = self._get_base_url(self.sitemap_url)
        
        self.logger.info(f"Initialized SitemapAnalyzer for {self.sitemap_url}")
        self.logger.info(f"Base URL extracted: {self.base_url}")

    def set_log_level(self, level):
        """Set the logging level for the analyzer.
        
        Args:
            level: Logging level (e.g., logging.DEBUG, logging.INFO, logging.WARNING)
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
        self.logger.info(f"Logging level set to {logging.getLevelName(level)}")

    def _get_base_url(self, url):
        """Extracts the base URL from a given URL."""
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"

    def _parse_robots_content(self, content):
        """Parse robots.txt content and extract URLs for analysis."""
        self.logger.info("Parsing robots.txt content for URLs")
        urls = []
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Extract URLs from various robots.txt directives
            if line.lower().startswith(('allow:', 'disallow:')):
                # Extract path from Allow/Disallow directives
                path = line.split(':', 1)[1].strip()
                if path and path != '/' and not path.startswith('*'):
                    # Convert relative path to absolute URL
                    if path.startswith('/'):
                        full_url = f"{self.base_url}{path}"
                        urls.append(full_url)
                        self.logger.debug(f"Extracted URL from robots.txt: {full_url}")
            
            elif line.lower().startswith('sitemap:'):
                # Still try to extract sitemap URLs even if we're using robots.txt
                sitemap_url = line.split(':', 1)[1].strip()
                self.logger.info(f"Found sitemap reference in robots.txt: {sitemap_url}")
                
                # Try to fetch and parse the sitemap
                try:
                    response = self.session.get(sitemap_url, timeout=10)
                    response.raise_for_status()
                    if 'xml' in response.headers.get('content-type', '').lower():
                        sitemap_urls = self._parse_sitemap_content(response.content, response.headers.get('content-type', ''))
                        urls.extend(sitemap_urls)
                        self.logger.info(f"Added {len(sitemap_urls)} URLs from referenced sitemap")
                except requests.exceptions.RequestException as e:
                    self.logger.warning(f"Could not fetch referenced sitemap {sitemap_url}: {e}")
        
        # If no URLs found from robots.txt, add common pages
        if not urls:
            self.logger.info("No specific URLs found in robots.txt, adding common pages")
            common_pages = ['/', '/about', '/contact', '/products', '/services', '/blog']
            for page in common_pages:
                urls.append(f"{self.base_url}{page}")
        
        self.logger.info(f"Extracted {len(urls)} URLs from robots.txt analysis")
        return urls

    def _parse_sitemap_content(self, content, content_type):
        """Parse sitemap content and extract URLs, handling both regular sitemaps and sitemap indexes."""
        # Check if this is robots.txt content
        if 'robots.txt' in self.sitemap_url or 'text/plain' in content_type.lower():
            self.logger.info("Detected robots.txt file, extracting URLs from robots directives")
            return self._parse_robots_content(content.decode('utf-8') if isinstance(content, bytes) else content)
        
        # Handle XML sitemaps
        soup = BeautifulSoup(content, 'xml')
        urls = []
        
        # Check if this is a sitemap index (contains sitemapindex tag)
        if soup.find('sitemapindex'):
            self.logger.info("Detected sitemap index file")
            # Extract sitemap URLs from the index
            sitemap_locs = soup.find_all('loc')
            sitemap_urls = [loc.text for loc in sitemap_locs]
            self.logger.info(f"Found {len(sitemap_urls)} sitemaps in index")
            
            # Fetch and parse each individual sitemap
            for sitemap_url in sitemap_urls:
                try:
                    self.logger.debug(f"Fetching individual sitemap: {sitemap_url}")
                    response = self.session.get(sitemap_url, timeout=10)
                    response.raise_for_status()
                    
                    # Parse the individual sitemap
                    individual_soup = BeautifulSoup(response.content, 'xml')
                    individual_urls = [loc.text for loc in individual_soup.find_all('loc')]
                    urls.extend(individual_urls)
                    self.logger.debug(f"Added {len(individual_urls)} URLs from {sitemap_url}")
                    
                except requests.exceptions.RequestException as e:
                    self.logger.warning(f"Failed to fetch individual sitemap {sitemap_url}: {e}")
                    continue
        else:
            # Regular sitemap - extract URLs directly
            self.logger.info("Detected regular sitemap file")
            urls = [loc.text for loc in soup.find_all('loc')]
        
        return urls

    def analyze(self):
        """Analyzes the sitemap and returns a report of issues."""
        self.logger.info("Starting sitemap analysis")
        start_time = time.time()
        
        try:
            self.logger.info(f"Fetching sitemap from {self.sitemap_url}")
            response = self.session.get(self.sitemap_url, timeout=10)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '').lower()
            self.logger.debug(f"Content type: {content_type}")
            
            # Parse sitemap content (handles both regular sitemaps and sitemap indexes)
            urls = self._parse_sitemap_content(response.content, content_type)
            self.logger.info(f"Found {len(urls)} URLs in total from sitemap(s)")
            
            if not urls:
                error_msg = "No URLs found in sitemap"
                self.logger.error(error_msg)
                return {"error": error_msg}
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching sitemap: {e}")
            return {"error": f"Error fetching sitemap: {e}"}
        except Exception as e:
            self.logger.error(f"Error parsing sitemap: {e}")
            return {"error": f"Error parsing sitemap: {e}"}

        self.logger.info("Starting parallel analysis tasks")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            self.logger.info("Submitting broken links detection task")
            broken_links_future = executor.submit(self.detect_broken_links, urls)
            
            self.logger.info("Submitting orphan pages detection task")
            orphan_pages_future = executor.submit(self.detect_orphan_pages, urls)
            
            self.logger.info("Submitting SEO issues detection task")
            seo_issues_future = executor.submit(self.detect_seo_issues, urls)

            broken_links = broken_links_future.result()
            orphan_pages = orphan_pages_future.result()
            seo_issues = seo_issues_future.result()

        end_time = time.time()
        self.logger.info(f"Analysis completed in {end_time - start_time:.2f} seconds")
        self.logger.info(f"Found {len(broken_links)} broken links, {len(orphan_pages)} orphan pages, {len(seo_issues)} SEO issues")

        return {
            "broken_links": broken_links,
            "orphan_pages": orphan_pages,
            "seo_issues": seo_issues
        }

    def _check_link(self, url):
        try:
            response = self.session.get(url, timeout=5)
            if response.status_code >= 400:
                self.logger.warning(f"Broken link detected: {url} (Status: {response.status_code})")
                return {"url": url, "status_code": response.status_code}
            else:
                self.logger.debug(f"Link OK: {url} (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Connection error for {url}: {e}")
            return {"url": url, "status_code": "Connection Error"}
        return None

    def detect_broken_links(self, urls):
        """Identifies and reports broken links."""
        self.logger.info(f"Starting broken links detection for {len(urls)} URLs")
        broken_links = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self._check_link, url) for url in urls]
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                if (i + 1) % 10 == 0:
                    self.logger.info(f"Checked {i + 1}/{len(urls)} links for broken status")
                result = future.result()
                if result:
                    broken_links.append(result)
        self.logger.info(f"Broken links detection completed. Found {len(broken_links)} broken links")
        return broken_links

    def detect_orphan_pages(self, urls):
        """Identifies and reports orphan pages."""
        self.logger.info(f"Starting orphan pages detection for {len(urls)} URLs")
        self.logger.info("Crawling website to discover internal links")
        internal_links = self.crawl_website()
        self.logger.info(f"Found {len(internal_links)} internal links during crawling")
        orphan_pages = [url for url in urls if url not in internal_links]
        self.logger.info(f"Orphan pages detection completed. Found {len(orphan_pages)} orphan pages")
        if orphan_pages:
            self.logger.warning(f"Orphan pages found: {orphan_pages[:5]}{'...' if len(orphan_pages) > 5 else ''}")
        return orphan_pages

    def _check_seo(self, url):
        try:
            response = self.session.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description_content = description_tag.get('content') if description_tag else None
            if not description_content or not description_content.strip():
                self.logger.debug(f"SEO issue detected: Missing meta description for {url}")
                return {"url": url, "issue": "Missing meta description"}
            else:
                self.logger.debug(f"SEO check passed: {url} has meta description")
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Error fetching page for SEO check {url}: {e}")
            return {"url": url, "issue": "Error fetching page"}
        return None

    def detect_seo_issues(self, urls):
        """Identifies and reports potential SEO issues (missing descriptions)."""
        self.logger.info(f"Starting SEO issues detection for {len(urls)} URLs")
        seo_issues = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self._check_seo, url) for url in urls]
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                if (i + 1) % 10 == 0:
                    self.logger.info(f"Checked {i + 1}/{len(urls)} pages for SEO issues")
                result = future.result()
                if result:
                    seo_issues.append(result)
        self.logger.info(f"SEO issues detection completed. Found {len(seo_issues)} SEO issues")
        return seo_issues

    def crawl_website(self):
      """Crawls the entire website to extract internal links."""
      self.logger.info(f"Starting website crawl from {self.base_url}")
      internal_links = set()
      self.visited = set()
      self.crawl_page(self.base_url, internal_links)
      self.logger.info(f"Website crawl completed. Discovered {len(internal_links)} internal links")
      return internal_links

    def crawl_page(self, url, internal_links):
      """Recursively crawls a single page and extracts links."""
      if url in self.visited:
        return

      self.visited.add(url)
      self.logger.debug(f"Crawling page: {url}")
      
      if len(self.visited) % 10 == 0:
          self.logger.info(f"Crawled {len(self.visited)} pages so far")
      
      try:
          response = self.session.get(url, timeout=5)
          response.raise_for_status()
          soup = BeautifulSoup(response.content, 'html.parser')
          links_found = 0
          for link in soup.find_all('a', href=True):
              absolute_url = urljoin(url, link['href'])
              if absolute_url.startswith(self.base_url):
                  if absolute_url not in internal_links:
                      internal_links.add(absolute_url)
                      links_found += 1
                  self.crawl_page(absolute_url, internal_links)
          self.logger.debug(f"Found {links_found} new internal links on {url}")
      except requests.exceptions.RequestException as e:
          self.logger.warning(f"Error crawling {url}: {e}")

    def _find_sitemap_url(self, url):
        """Find the actual sitemap URL by checking robots.txt or common locations."""
        self.logger.info(f"Attempting to find sitemap URL from: {url}")
        
        # If URL already ends with sitemap.xml, try it first
        if url.endswith('sitemap.xml'):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                # Check if it's actually XML content
                if 'xml' in response.headers.get('content-type', '').lower():
                    self.logger.info(f"Found valid sitemap at: {url}")
                    return url
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Failed to fetch sitemap at {url}: {e}")
        
        # Try to find sitemap from robots.txt
        base_url = self._get_base_url(url)
        robots_url = f"{base_url}/robots.txt"
        
        self.logger.info(f"Checking robots.txt at: {robots_url}")
        try:
            response = self.session.get(robots_url, timeout=10)
            response.raise_for_status()
            robots_content = response.text
            
            # Look for sitemap declarations in robots.txt
            for line in robots_content.split('\n'):
                line = line.strip()
                if line.lower().startswith('sitemap:'):
                    sitemap_url = line.split(':', 1)[1].strip()
                    self.logger.info(f"Found sitemap URL in robots.txt: {sitemap_url}")
                    
                    # Verify the sitemap URL works
                    try:
                        sitemap_response = self.session.get(sitemap_url, timeout=10)
                        sitemap_response.raise_for_status()
                        if 'xml' in sitemap_response.headers.get('content-type', '').lower():
                            return sitemap_url
                    except requests.exceptions.RequestException:
                        self.logger.warning(f"Sitemap URL from robots.txt is not accessible: {sitemap_url}")
                        continue
        
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"Failed to fetch robots.txt: {e}")
        
        # Try common sitemap locations
        common_sitemap_paths = [
            '/sitemap.xml',
            '/sitemap_index.xml',
            '/sitemaps.xml',
            '/sitemap1.xml'
        ]
        
        self.logger.info("Trying common sitemap locations")
        for path in common_sitemap_paths:
            test_url = f"{base_url}{path}"
            try:
                response = self.session.get(test_url, timeout=10)
                response.raise_for_status()
                if 'xml' in response.headers.get('content-type', '').lower():
                    self.logger.info(f"Found sitemap at common location: {test_url}")
                    return test_url
            except requests.exceptions.RequestException:
                self.logger.debug(f"No sitemap found at: {test_url}")
                continue
        
        # Final fallback: use robots.txt as source for URLs if no sitemap found
        self.logger.warning("No sitemap found, falling back to robots.txt for URL extraction")
        return robots_url