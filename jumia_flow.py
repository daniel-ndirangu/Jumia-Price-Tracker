import subprocess  
from prefect import task,flow,get_run_logger
import os
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jumiascraper.spiders.samsung import SamsungSpider
from prefect.client.schemas.schedules import IntervalSchedule, CronSchedule
from prefect.blocks.system import Secret



@task(retries=2)
def run_query():
    logger = get_run_logger()
    logger.info("Starting Scrapy spider...")
    
    
    # # Fetch the MONGOAT_URI secret from Prefect
    # mongo_uri = Secret.load("mongoat-uri").get()
    
    settings = get_project_settings()
    
    # settings.set('MONGO_URI', mongo_uri)  
    # settings.set('MONGO_DATABASE', 'ecommerce_db')
    # settings.set('MONGO_COLLECTION', 'samsung_timeseries')
    
   
    process = CrawlerProcess(settings)
    process.crawl(SamsungSpider)
    process.start()
    logger.info("Scrapy spider finished.")


@flow
def run_all_task():
    run_query()


  

if __name__ == "__main__":
  run_all_task.from_source(
    source="https://github.com/daniel-ndirangu/Jumia-Price-Tracker.git",
    entrypoint="jumia_flow.py:run_all_task", 
     ).deploy(
       name="my-first-deployment",
       work_pool_name="my-work-pool",
       job_variables={"pip_packages": ["scrapy", "scrapy-playwright", "pymongo", "w3lib", "datetime"]},
       cron = "0 20 * * *"
       )

    