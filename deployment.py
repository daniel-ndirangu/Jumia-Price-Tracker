from prefect import flow
from prefect.client.schemas.schedules import CronSchedule

if __name__ == "__main__":
     schedule = CronSchedule(
        cron="10 15 * * *",
        timezone="Africa/Nairobi"
    )
     
     flow.from_source(
        source="https://github.com/daniel-ndirangu/Jumia-Price-Tracker.git",
        entrypoint="jumia_flow.py:run_all_task"
    ).deploy(
        name = "first-jumia-deployment",
        work_pool_name ="jumia-managed-pool",
        tags = ["jumia", "scraping"],
        job_variables = {"pip_packages": {"pymongo", "scrapy"}}
    )
     
   

   