import scrapy
import json


class KilimallSpider(scrapy.Spider):
    name = 'kilimall'
    allowed_domains = ['api.kilimall.com']
    # Scraping from kilimall api instead of website
    start_urls = ['https://api.kilimall.com/ke/v1/product/search']

    def parse(self, response):
        data = json.loads(response.body)
        yield from data['data']['products']

        next_page = data['links']['next']
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)
