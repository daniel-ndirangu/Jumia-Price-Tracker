import subprocess  
from prefect import task,flow,get_run_logger
import os



@task(retries=2)
def run_query():
  query = 'scrapy crawl products'
  proc = subprocess.Popen(query, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, )
  stdout, stderr = proc.communicate()
  if proc.returncode != 0:
    raise Exception(stderr.decode())
   

@flow
def run_all_task():
  run_query()

  

if __name__ == "__main__":
  run_all_task.from_source(
    source="https://github.com/daniel-ndirangu/Jumia-Price-Tracker.git",
    entrypoint="jumia_flow.py:run_all_task"
     ).deploy(
       name="my-first-deployment",
       work_pool_name="my-work-pool",
       job_variables={"pip_packages": ["scrapy", "python-dotenv", "scrapy-playwright", "pymongo", "w3lib", "datetime"]},
       cron="40 3 * * *")

    