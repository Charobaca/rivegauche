import scrapy
from rivegauche.items import RivegaucheItem
from urllib.parse import urljoin
import re


class RiveSpider(scrapy.Spider):
    name = 'rive'
    start_urls = [
        'https://api.rivegauche.ru/cms/v1/newRG/navigation/Rg2_Catalog_Node']


    def parse(self, response):

        categories = response.json()['children'][0:-1]

        for item in categories:
            href = item['linkUrl']
            print(href)

            category_name = item['linkName']

            yield scrapy.Request(url=f'https://rivegauche.ru{href}', callback=self.parse_page, meta={'category_name': category_name})


    def parse_page(self, response):
        category_name = response.meta.get('category_name')
        code = response.xpath('//script[@id="rg-shop-ngx-state"]').get()

        category_code = re.findall(r'categoryCode&q;:&q;+([a-zA-Z]+)', code)[0]

        yield scrapy.Request(url = f'https://api.rivegauche.ru/rg/v1/newRG/products/search?fields=FULL&currentPage=0&pageSize=100&categoryCode={category_code}', callback = self.get_api, meta = {'category_name': category_name, 'category_code': category_code})

    def get_api(self, response):
        category_name = response.meta.get('category_name')
        category_code = response.meta.get('category_code')
        pagination = response.json()['pagination']['totalPages']

        results = {
                'all_results': response.json()['results'],
                'category_name': category_name
                }

        item = RivegaucheItem()
        item['results'] = results

        yield item

        for page in range(1, pagination):
            yield scrapy.Request(url = f'https://api.rivegauche.ru/rg/v1/newRG/products/search?fields=FULL&currentPage={page}&pageSize=100&categoryCode={category_code}', callback = self.parse_api, meta = {'category_name': category_name})

    def parse_api(self, response):
        category_name = response.meta.get('category_name')

        results = {
                'all_results': response.json()['results'],
                'category_name': category_name
        }

        item = RivegaucheItem()
        item['results'] = results

        yield item
