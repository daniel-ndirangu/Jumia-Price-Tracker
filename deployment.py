from prefect import flow
from prefect.schedules import CronSchedule


if __name__ == "__main__":
    schedule = CronSchedule(
        cron="35 16 * * *",
        timezone="Africa/Nairobi"
    )

    flow.from_source(
        source="https://github.com/daniel-ndirangu/Jumia-Price-Tracker.git",
        entrypoint="flow.py:scrape_jumia"
    ).deploy(
        name="jumia_scraper",
        work_pool_name="jumia-managed-pool",
        schedule=schedule
    )