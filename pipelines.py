# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo


class RivegauchePipeline:
    def __init__(self):
        connection = pymongo.MongoClient(
            'localhost',
            27017,
        )

        db = connection['rivegauche']
        self.collection = db['products']

    def process_item(self, item, spider):

        category_name = item['results']['category_name']
        results = item['results']['all_results']

        for result in results:
            commit = {
                'category_name': category_name,
                'product_data': result
            }
            self.collection.insert_one(commit)

        return item
