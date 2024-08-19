from prefect import flow, task
import subprocess


@task(retries=1)
def run_spider():
    subprocess.run(["scrapy", "crawl", "products"])
    
@flow
def scrape_jumia():
    run_spider()