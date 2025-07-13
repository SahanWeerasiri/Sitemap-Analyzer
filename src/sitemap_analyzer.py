import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class SitemapAnalyzer:
    def __init__(self, sitemap_url):
        """Initializes the SitemapAnalyzer with the sitemap URL."""
        self.sitemap_url = sitemap_url
        self.base_url = self._get_base_url(sitemap_url)
        self.visited = set()

    def _get_base_url(self, url):
        """Extracts the base URL from a given URL."""
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}"

    def analyze(self):
        """Analyzes the sitemap and returns a report of issues."""
        try:
            response = requests.get(self.sitemap_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            urls = [loc.text for loc in soup.find_all('loc')]
        except requests.exceptions.RequestException as e:
            return {"error": f"Error fetching sitemap: {e}"}

        broken_links = self.detect_broken_links(urls)
        orphan_pages = self.detect_orphan_pages(urls)
        seo_issues = self.detect_seo_issues(urls)

        return {
            "broken_links": broken_links,
            "orphan_pages": orphan_pages,
            "seo_issues": seo_issues
        }

    def detect_broken_links(self, urls):
        """Identifies and reports broken links."""
        broken_links = []
        for url in urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code >= 400:
                    broken_links.append({"url": url, "status_code": response.status_code})
            except requests.exceptions.RequestException:
                broken_links.append({"url": url, "status_code": "Connection Error"})
        return broken_links

    def detect_orphan_pages(self, urls):
        """Identifies and reports orphan pages."""
        internal_links = self.crawl_website()
        orphan_pages = [url for url in urls if url not in internal_links]
        return orphan_pages

    def detect_seo_issues(self, urls):
        """Identifies and reports potential SEO issues (missing descriptions)."""
        seo_issues = []
        for url in urls:
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                description_tag = soup.find('meta', attrs={'name': 'description'})
                description_content = description_tag.get('content') if description_tag else None
                if not description_content or not description_content.strip():
                    seo_issues.append({"url": url, "issue": "Missing meta description"})
            except requests.exceptions.RequestException:
                seo_issues.append({"url": url, "issue": "Error fetching page"})
        return seo_issues

    def crawl_website(self):
      """Crawls the entire website to extract internal links."""
      internal_links = set()
      self.crawl_page(self.base_url, internal_links)
      return internal_links

    def crawl_page(self, url, internal_links):
      """Recursively crawls a single page and extracts links."""
      if url in self.visited:
        return

      self.visited.add(url)
      try:
          response = requests.get(url, timeout=5)
          response.raise_for_status()
          soup = BeautifulSoup(response.content, 'html.parser')
          for link in soup.find_all('a', href=True):
              absolute_url = urljoin(url, link['href'])
              if self.base_url in absolute_url:
                  internal_links.add(absolute_url)
                  self.crawl_page(absolute_url, internal_links)
      except requests.exceptions.RequestException as e:
          print(f"Error crawling {url}: {e}")