from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/daniel-ndirangu/Jumia-Price-Tracker.git",
        entrypoint="flow.py:scrape_jumia"
    ).deploy(
        name = "jumia_scraper",
        work_pool_name="jumia-managed-pool",
        cron="20 16 * * *"
    )