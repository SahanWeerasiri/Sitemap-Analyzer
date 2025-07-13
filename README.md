# Sitemap Analyzer

A backend service (Python) for analyzing website sitemaps, identifying broken links, orphan pages, and potential SEO issues. Provides both API and CLI interfaces.

## Key Features

*   **Broken Link Detection:** Identifies and reports broken links within the sitemap.
*   **Orphan Page Detection:** Detects pages not linked to from within the sitemap.
*   **SEO Analysis:** Provides insights into potential SEO issues (e.g., missing titles, descriptions).
*   **Customizable Crawl Depth:** Configure how deep the analyzer crawls the website.
*   **Detailed Reporting:** Generates comprehensive reports in various formats (e.g., JSON, CSV).

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

## Example

```bash
python main.py --mode cli analyze --sitemap_url https://example.com/sitemap.xml --output_format json --output_file report.json
```

## License

[Specify the License used, e.g., MIT License]