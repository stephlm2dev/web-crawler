# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy_scraper.items import ScrapyScraperItem


class WebsiteSpider(CrawlSpider):
    name = 'website'
    allowed_domains = ['stephlm2dev.github.io']
    start_urls = ['https://stephlm2dev.github.io/']

    already_fetched_urls = []

    # This spider has one rule: extract all (unique and canonicalized) links,
    # follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback='parse_items',
            process_links='remove_unwanted_links'
        )
    ]

    # Method which starts the requests by visiting all URLs specified
    # in start_urls
    def start_requests(self):
        for url in self.start_urls:
            self.already_fetched_urls.append(url)

            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def remove_unwanted_links(self, links):
        for link in links:
            if self.go_to_this_page(link.url):
                yield link

    def go_to_this_page(self, url):
        ko_extension = self.rejected_extension(url)
        ko_path = self.rejected_path(url)
        ok_domain = self.authorised_domain(url)
        crawled = self.already_fetched(url)
        # print('Extension: ', not ko_extension)
        # print('Path: ', not ko_path)
        # print('Domain: ', ok_domain)
        # print('Crawled: ', not crawled)

        return ok_domain and not ko_path and not ko_extension and not crawled

    def rejected_extension(self, url):
        rejected_extensions = [
            '.css', '.js', '.pdf', '.php', '.gif'
        ]
        return any(ext in url for ext in rejected_extensions)

    def rejected_path(self, url):
        rejeted_paths = [
            '?custom-css=', '/trackback', 'http://',
            '/robots.txt', '/feed', '/plugins/'
        ]
        return any(path in url for path in rejeted_paths)

    def authorised_domain(self, url):
        return any(url.startswith('https://' + ok_domain) for ok_domain in self.allowed_domains)

    def already_fetched(self, url):
        # print('Fetched urls: ', self.already_fetched_urls)
        return url in self.already_fetched_urls

    # Method for parsing items
    def parse_items(self, response):
        # The list of items that are found on the particular page
        items = []
        # Only extract canonicalized and unique links
        # (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(
                response
        )

        # Now go through all the found links
        for link in links:
            # Check whether the domain of the URL of the link is allowed;
            # so whether it is in one of the allowed domains
            url = link.url.rstrip('/')
            # print('Current link: ', url)

            is_allowed = self.go_to_this_page(url)

            # print('OK ?', is_allowed)

            # If it is allowed, create a new item and add it to the
            # list of found items
            if is_allowed:
                self.already_fetched_urls.append(url)

                item = ScrapyScraperItem()
                item['url'] = url
                items.append(item)
        # Return all the found items
        return items
