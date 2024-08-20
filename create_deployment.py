from prefect import flow
from prefect.client.schemas.schedules import CronSchedule


if __name__ == "__main__":
    schedule = CronSchedule(
        cron="00 16 * * *",
        timezone="Africa/Nairobi"
    )

    flow.from_source(
        source="https://github.com/daniel-ndirangu/Jumia-Price-Tracker.git",
        entrypoint="jumia_flow.py:scrape_jumia"
    ).deploy(
        name="jumia-scraping-deployment",
        work_pool_name="jumia-scraping-pool",
        schedule=schedule,
        tags=["scraping", "jumia"],
        job_variables={"pip_packages": ["scrapy", "pymongo", "datetime"]},
        build=False
        )