from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/daniel-ndirangu/Jumia-Price-Tracker.git",
        entrypoint="jumia_flow.py:run_all_task",
    ).deploy(
        name="my-first-deployment",
        work_pool_name="my-managed-pool",
        cron="0 20 * * *",
        job_variables={"pip_packages": ["scrapy", "scrapy-playwright", "python-dotenv", "pymongo"]}
    )