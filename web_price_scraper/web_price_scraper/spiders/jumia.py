import scrapy
from web_price_scraper.items import WebScraperItem
from scrapy.loader import ItemLoader


class JumiaSpider(scrapy.Spider):
    name = 'jumia'
    allowed_domains = ['jumia.co.ke']
    start_urls = ['http://jumia.co.ke/']

    def parse(self, response):
        for link in response.css('div.flyout a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_categories)

    def parse_categories(self, response):

        products = response.css('article.prd._fb.col.c-prd')

        for product in products:

            l = ItemLoader(item = WebScraperItem(), selector=product)

            l.add_css('category', 'a.core::attr(data-category)')
            l.add_css('name', 'h3.name')
            l.add_css('price', 'div.prc')
            l.add_css('product_link', 'a.core::attr(href)')
            l.add_css('img_link', 'img::attr(data-src)')

            ##### RATING ####
            #         response.css("#jm > main > div.aim.row.-pbm > div.-pvs.col12 > section > div.-paxs.row._no-g._4cl-3cm-shs > article:nth-child(37) > a > div.info > div.rev > div.stars._s::text").get().replace(" out of 5", "")

            yield l.load_item()

        # Pagination
        next_page = 'http://jumia.co.ke'+response.css("#jm > main > div.aim.row.-pbm > div.-pvs.col12 > section > div.pg-w.-ptm.-pbxl > a:nth-child(6)").attrib["href"]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_categories)
        else:
            pass
