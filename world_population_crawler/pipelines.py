# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class WorldPopulationCrawlerPipeline(object):
    collection_name = "world_population"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://huwngnosleep:abcdAbcd@cluster0.vidnk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.db = self.client["world_population"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
