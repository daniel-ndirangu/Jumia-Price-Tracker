from prefect import flow, task
import subprocess
import scrapy 


@task
def run_spider():
    return subprocess.run(["scrapy", "crawl", "products"])
    
@flow
def scrape_jumia():
    return run_spider()
    
       
if __name__ == "__main__":
    scrape_jumia()
    