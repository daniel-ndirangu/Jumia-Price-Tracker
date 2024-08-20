from prefect import flow, task
import subprocess  


@task
def run_spider():
    return subprocess.run(["scrapy", "crawl", "products"])
    
@flow
def scrape_jumia():
    run_spider()
    
       
if __name__ == "__main__":
    scrape_jumia()
    