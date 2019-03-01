# Scrapy

This tool list all links for a website

Based on [Scrapy](https://scrapy.org)

## Installation

```bash
pip install scrapy
```

## Usage

```bash
scrapy crawl website -o links.csv -t csv
```

## Development

You can edit output fields in `scrapy_scraper/items.py`.

You can edit website URL and filter conditions in `scrapy_scraper/spiders/website.py`.
