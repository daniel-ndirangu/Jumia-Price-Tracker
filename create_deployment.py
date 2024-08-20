from prefect import flow
from prefect.client.schemas.schedules import CronSchedule


if __name__ == "__main__":
    schedule = CronSchedule(
        cron="0 13 * * *",
        timezone="Africa/Nairobi"
    )

    flow.from_source(
        source="https://github.com/daniel-ndirangu/Jumia-Price-Tracker.git",
        entrypoint="jumia_flow.py:scrape_jumia"
    ).deploy(
        name="jumia_scraper",
        work_pool_name="jumia-managed-pool",
        schedule=schedule,
        build=False
    )