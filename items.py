# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader


class RivegaucheItem(scrapy.Item):
    results = scrapy.Field()
