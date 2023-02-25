import scrapy


class ShopitSpider(scrapy.Spider):
    name = 'shopit'
    allowed_domains = ['shopit.co.ke']
    start_urls = ['http://shopit.co.ke/']

    def parse(self, response):
        for link in response.css('div.ut2-menu__inbox a::attr(href)').getall():
            if link != 'javascript:void(0)':
                if link == './categories/':
                    pass
                else:
                    yield response.follow(link, callback=self.parse_categories)

    def parse_categories(self, response):
        products = response.css('div.ty-column4')
        for product in products:
            yield {
                'name': product.css('a.product-title::text').get(),
                'price': product.css('span.ty-price-num::text')[1::2].get(),
                'product_link': product.css('div.ut2-gl__name a::attr(href)').get(),
                'img_link': product.css('img::attr(data-src)').get(),
            }

        next_page = response.css('a.ty-pagination__item.ty-pagination__btn.ty-pagination__next.cm-history.cm-ajax.ty-pagination__right-arrow::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_categories)
