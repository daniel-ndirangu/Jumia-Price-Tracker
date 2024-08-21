from prefect import flow, task
import subprocess  


# @task
# def run_spider():
#     return subprocess.run(["scrapy", "crawl", "products"], capture_output=True)
    
# @flow
# def scrape_jumia():
#     run_spider()
       
# if __name__ == "__main__":
#     scrape_jumia()


from prefect import flow
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jumiascraper.spiders.samsung import SamsungSpider

# Import your settings module
from jumiascraper.settings import *

@flow
def run_scraper():
    
    # Create a Settings object and populate it with your settings
    settings = Settings({
        "BOT_NAME": BOT_NAME,
        "SPIDER_MODULES": SPIDER_MODULES,
        "NEWSPIDER_MODULE": NEWSPIDER_MODULE,
        "DOWNLOAD_HANDLERS": DOWNLOAD_HANDLERS,
        "TWISTED_REACTOR": TWISTED_REACTOR,
        "MONGO_URI": MONGO_URI,
        "MONGO_DATABASE": MONGO_DATABASE,
        "MONGO_COLLECTION": MONGO_COLLECTION,
        "USER_AGENT": USER_AGENT,
        "ROBOTSTXT_OBEY": ROBOTSTXT_OBEY,
        "DOWNLOAD_DELAY": DOWNLOAD_DELAY,
        "COOKIES_ENABLED": COOKIES_ENABLED,
        "ITEM_PIPELINES": ITEM_PIPELINES,
        "AUTOTHROTTLE_ENABLED": AUTOTHROTTLE_ENABLED,
        "AUTOTHROTTLE_START_DELAY": AUTOTHROTTLE_START_DELAY,
        "AUTOTHROTTLE_MAX_DELAY": AUTOTHROTTLE_MAX_DELAY,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": AUTOTHROTTLE_TARGET_CONCURRENCY,
        "FEED_EXPORT_ENCODING": FEED_EXPORT_ENCODING,
    })
    
    
    process = CrawlerProcess(settings=settings)
    process.crawl(SamsungSpider)
    process.start()
    
if __name__ == "__main__":
    run_scraper()
    