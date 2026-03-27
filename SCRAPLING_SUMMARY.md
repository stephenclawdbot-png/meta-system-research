# 🕷️ Scrapling - Advanced Web Scraping Framework

## Project Overview
**Scrapling** is an adaptive web scraping framework by Karim Shoair that handles everything from single requests to full-scale crawling operations. It features intelligent parsing, anti-bot bypass, and sophisticated session management.

## Key Features

### 🎯 Core Capabilities
- **Adaptive Parsing**: Learns from website changes and relocates elements automatically
- **Cloudflare Bypass**: Out-of-the-box support for Turnstile and other anti-bot systems
- **Multi-Session Spiders**: Concurrent crawling with pause/resume functionality
- **Advanced Fetchers**: HTTP, stealth, and dynamic browser-based fetching

### 🚀 Performance Highlights
- **Blazing Fast**: 10x faster than standard libraries
- **Memory Efficient**: Optimized data structures with lazy loading
- **Type Coverage**: Full type hints with PyRight/MyPy validation
- **92% Test Coverage**: Battle-tested by hundreds of web scrapers

## Installation Options

### Basic Installation
```bash
pip install scrapling
```

### Full Installation
```bash
pip install "scrapling[all]"
scrapling install
```

### Docker
```bash
docker pull pyd4vinci/scrapling
```

## Quick Start Examples

### Basic HTTP Fetching
```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()
```

### Stealth Mode (Cloudflare Bypass)
```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch('https://nopecha.com/demo/cloudflare')
data = page.css('#padded_content a').getall()
```

### Full Spider Crawling
```python
from scrapling.spiders import Spider, Response

class QuotesSpider(Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com/"]
    
    async def parse(self, response: Response):
        for quote in response.css('.quote'):
            yield {
                "text": quote.css('.text::text').get(),
                "author": quote.css('.author::text').get(),
            }

result = QuotesSpider().start()
print(f"Scraped {len(result.items)} quotes")
result.items.to_json("quotes.json")
```

## Advanced Features

### Adaptive Element Finding
```python
# Automatically relocates elements when sites change
products = p.css('.product', adaptive=True)
```

### Multi-Session Management
```python
class MultiSessionSpider(Spider):
    def configure_sessions(self, manager):
        manager.add("fast", FetcherSession(impersonate="chrome"))
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)
```

### MCP Server Integration
Built-in Model Context Protocol server for AI-assisted web scraping with reduced token usage.

## CLI Tool
Extract content directly from command line:
```bash
scrapling extract get 'https://example.com' content.md
scrapling shell  # Interactive scraping shell
```

## Performance Benchmarks
Scrapling consistently outperforms popular libraries:
- **2.02ms** (Scrapling) vs **1,584.31ms** (BeautifulSoup)
- **784x faster** than BeautifulSoup with lxml
- **41x faster** than Selectolax

## Architecture Benefits
- **Scalable**: Single requests to concurrent crawls
- **Robust**: Auto-retry on blocked requests
- **Flexible**: CSS, XPath, text, regex, and similarity-based selection
- **Professional**: Enterprise-grade proxy rotation and session management

## Ideal Use Cases
- **Data Mining**: Large-scale content extraction
- **Research**: Academic and market research
- **Monitoring**: Competitive intelligence and price tracking
- **Automation**: Workflow integration and data pipelines

## Compliance Notes
⚠️ Use responsibly - always respect websites' terms of service and robots.txt files.

## Repository Structure
```
Scrapling/
├── scrapling/
│   ├── fetchers/        # HTTP, stealth, dynamic fetching
│   ├── spiders/         # Full crawling framework
│   ├── parser/          # Adaptive parsing engine
│   └── cli/            # Command-line interface
├── docs/               # Multi-language documentation
└── benchmarks/         # Performance testing
```

## Documentation
- 📚 Full Documentation: https://scrapling.readthedocs.io
- 🎥 Demo Video: https://www.youtube.com/watch?v=qyFk3ZNwOxE
- 💬 Discord: https://discord.gg/EMgGbDceNQ
- 🐦 Twitter: https://x.com/Scrapling_dev

## Author
**Karim Shoair** - Creator and maintainer

Scrapling represents state-of-the-art web scraping technology with professional-grade features suitable for enterprise data extraction workflows.