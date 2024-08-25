from prefect import task,flow,get_run_logger
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jumiascraper.spiders.samsung import SamsungSpider
from prefect.client.schemas.schedules import IntervalSchedule, CronSchedule
from prefect.blocks.system import Secret
from datetime import timedelta, datetime



@task(retries=2)
def run_query():
    """Create prefect task scrapy script"""
    logger = get_run_logger()
    logger.info("Starting Scrapy spider...")
    
    settings = get_project_settings()
    
    process = CrawlerProcess(settings)
    process.crawl(SamsungSpider)
    process.start()
    logger.info("Scrapy spider finished.")


@flow
def run_all_task():
    """Create prefect flow from above task """
    run_query()
    


    