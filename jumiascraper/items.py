# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags

def clean_price(value):
    """remove the currency and commas from the values"""
    try:
        clean_value = value.split()[1].replace(",", "")
        return int(clean_value)
    except Exception as e:
        return value
    
def remove_percentage(value):
    """remove the percentage sign"""
    try:
        clean_value = value.replace("%", "")
        return int(clean_value)
    except Exception as e:
        return value
    
def add_root_url(url):
    """add the base url"""
    try:
        whole_url = f"https://www.jumia.co.ke{url}"
        return whole_url
    except Exception as e:
        return url

class JumiascraperItem(scrapy.Item):
    
    product = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    
    current_price = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, clean_price),
        output_processor = TakeFirst()
    )
    
    original_price = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, clean_price),
        output_processor = TakeFirst()
    )
    
    store = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    
    brand = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip),
        output_processor = TakeFirst()
    )
    
    store_discount = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, remove_percentage),
        output_processor = TakeFirst()
    )
    
    timestamp = scrapy.Field()
    
    url = scrapy.Field(
        input_processor = MapCompose(remove_tags, str.strip, add_root_url),
        output_processor = TakeFirst()
    )
