# SEO Analyzer Tool

A comprehensive Python-based SEO analyzer tool designed to evaluate website performance, SEO readiness, and more. Built using `asyncio`, `aiohttp`, `tkinter`, and `BeautifulSoup`.

## Features

- **Website Analysis:** Fetch and analyze website content asynchronously for SEO insights.
- **SEO Metrics:** Extract and evaluate critical SEO factors including:
  - Title and Meta Description
  - Page Load Time
  - Images Without Alt Tags
  - Broken Links
  - Canonical URL
  - Sitemap and Robots.txt Availability
  - SSL/TLS Configuration
- **Progress Feedback:** Provides a real-time progress bar during analysis.
- **Result Display:** Neatly displays results in a separate window.
- **Save Reports:** Save SEO analysis results in JSON format for future reference.

## Requirements

- Python 3.7+
- Libraries:
  - `asyncio`
  - `aiohttp`
  - `beautifulsoup4`
  - `tkinter`
  - `ssl`
  - `json`

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python seo_analyzer.py
   ```

## How to Use

1. Launch the application.
2. Enter the URL of the website you want to analyze.
3. Click the "Analyze" button to start the analysis.
4. View the detailed results in a new window.
5. Save the report as a JSON file if needed.

## Example

Analyze a website by entering its URL:

```
http://example.com
```

Results include:
- Title: Example Domain
- Meta Description: Example Domain provides a simple example...
- Load Time: 1.23 seconds
- Images without Alt: 5
- Broken Links: 2

## File Structure

- `seo_analyzer.py`: Main script.
- `requirements.txt`: List of required Python libraries.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

