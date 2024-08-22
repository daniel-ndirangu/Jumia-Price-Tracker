# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime
from pymongo.mongo_client import MongoClient
import logging
from pymongo.errors import PyMongoError
from prefect import task,flow,get_run_logger


# class JumiascraperPipeline:
#     def process_item(self, item, spider):
#         return item


class TimestampPipeline:
    def process_item(self, item, spider):
        item['timestamp'] = datetime.now()  # Adding timestamp
        return item
    
class NoDuplicateProductsPipeline:
    def __init__(self):
        self.products_seen = set()
        
    def process_item(self, item, spider):
        if item["product"] in self.products_seen:
            raise DropItem(f"Duplicate product found: {item}")
        else:
            self.products_seen.add(item["product"])
            return item
        
        
class MongoDBTimeSeriesPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        # Pull settings from the Scrapy settings
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        
        ## Check if the collection already exists
        if self.mongo_collection not in self.db.list_collection_names():
            self.collection = self.db[self.mongo_collection]
            
            self.db.create_collection(
                self.mongo_collection,
                timeseries={
                    "timeField": "timestamp",
                    "metaField": "metadata"
                }
            )
            
        self.collection = self.db[self.mongo_collection]

    # def close_spider(self, spider):
    #     self.client.close()

    def process_item(self, item, spider):
        
        # set the timestamp
        
        #logging.info(f"Processing item: {item['product']}") ** added
        
        timestamp = item.get("timestamp")
      

        # set the metadata 
        metadata = {
            "store": item.get("store"),
            "brand": item.get("brand"),
            "product": item.get("product")
        }
       
        # set the measurements
        measurements = {
            "current_price": item.get("current_price"),
            "original_price": item.get("original_price"),
            "store_discount": item.get("store_discount")
        }
        
        #Combine into one time series document
        time_series_data = {
            "timestamp": timestamp,
            "metadata": metadata,
            "measurements": measurements
        }

        # Insert the item into the time series collection
        self.collection.insert_one(dict(item))      # Initial
        
        # try:
        #      result = self.collection.insert_one(dict(item))
        #      logging.info(f"Item inserted with ID: {result.inserted_id}")
             
        # except PyMongoError as e:
        #     logging.error(f"Error inserting item into MongoDB: {e}")
        
        return item
    
    def close_spider(self, spider):
        # logging.info("Closing MongoDB connection")
        self.client.close()