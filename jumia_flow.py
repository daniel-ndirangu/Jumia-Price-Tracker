import subprocess  
import dotenv
from prefect import task,flow,get_run_logger
import os
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jumiascraper.spiders.samsung import SamsungSpider
from prefect.client.schemas.schedules import IntervalSchedule, CronSchedule


schedule = CronSchedule(timezone="Africa/Nairobi", cron="30, 7 * * *")


@task(retries=2)
def run_query():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(SamsungSpider)
    process.start()


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
       job_variables={"pip_packages": ["scrapy", "python-dotenv", "scrapy-playwright", "pymongo", "w3lib", "datetime"]}, 
       schedule=schedule
       )

    