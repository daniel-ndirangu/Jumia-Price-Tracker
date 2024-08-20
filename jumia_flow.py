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

@flow
def run_scraper():
    process = CrawlerProcess()
    process.crawl(SamsungSpider)
    process.start()
    
if __name__ == "__main__":
    run_scraper()
    