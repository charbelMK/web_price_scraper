# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

def make_url(value):
    return value.replace('/','http://jumia.co.ke/')

def make_price(value):
    return value.replace('KSh ','')

class WebScraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    category = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(remove_tags,make_price), output_processor = TakeFirst())
    product_link = scrapy.Field(input_processor = MapCompose(make_url), output_processor = TakeFirst())
    img_link = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
