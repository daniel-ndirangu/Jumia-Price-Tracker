from prefect import task,flow,get_run_logger
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jumiascraper.spiders.samsung import SamsungSpider
from prefect.client.schemas.schedules import IntervalSchedule, CronSchedule
from prefect.blocks.system import Secret
from datetime import timedelta, datetime
from prefect.blocks.system import Secret
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@task(retries=2)
def scrape_data():
    """Create prefect task scrapy script"""
    logger = get_run_logger()
    logger.info("Starting Scrapy spider...")
    
    settings = get_project_settings()
    
    process = CrawlerProcess(settings)
    process.crawl(SamsungSpider)
    process.start()
    logger.info("Scrapy spider finished.")
    
#Added to allow notifications
@task
def load_data():
    """Create a pandas dataframe from mongo collection"""
    #Connect to the database
    uri = Secret.load("mongo-uri").get()
    client = MongoClient(uri, server_api=ServerApi("1"))
    db = client["ecommerce_db"]
    collection = db["samsung_timeseries"]
    data = list(collection.find())
    df = pd.DataFrame(data)
    return df

@task
def get_price_difference(df):
    """Get the price difference between scraping subsequent runs
    """
    df = df.sort_values(by=["product", "timestamp"])
    
    latest_entries = df.groupby("product").tail(2)
    
    previous_data = latest_entries.groupby("product").head(1)
    
    current_data = latest_entries.groupby("product").tail(1)
    
    comparison_df = pd.merge(previous_data, current_data, on="product", suffixes=("_previous", "_latest"), how="inner")
    
    comparison_df["price_difference"] = comparison_df["current_price_latest"] - comparison_df["current_price_previous"]
    
    comparison_df["Price_change"] = (comparison_df["price_difference"] / comparison_df["current_price_latest"]) * 100
    
    comparison_df.rename({"timestamp_latest": "Updated_at", "current_price_latest": "Price", "product": "Product", "url_latest": "url"}, inplace=True, axis=1)
    
    return comparison_df

@task
def send_email(subject, body, to_email):
    """Send an email using Gmail SMTP"""
    from_email = Secret.load("from-email").get()
    email_pass = Secret.load("email-password").get()
    password = email_pass
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()


@task
def check_discounts_and_notify(comparison_df):
    "Check is they're discount and email if found"
    
    my_email = Secret.load("to-email").get()
    
    # Filter for discounts above 50%
    high_discounts = comparison_df[comparison_df['Price_change'] >= 20]
    
    if not high_discounts.empty:
        subject = "Samsung Discount Alert!!"
        body = "The following products have discounts above > 20:\n\n"
        for _, row in high_discounts.iterrows():
            body += f"Product: {row['Product']}\n"
            body += f"Current Price: Ksh {row['Price']:.2f}\n"
            body += f"Discount: {abs(row['Price_change']):.2f}%\n"
            body += f"Link: {row['url']}\n\n"
        
        send_email(subject, body, my_email)
        print("Email sent for high discounts!")
    else:
        print("No discounts above 50% found.")



@flow
def run_flow():
    """Create prefect flow from above tasks """    
    scrape_data()
    df = load_data()
    comparison_df = get_price_difference(df)
    check_discounts_and_notify(comparison_df)
    
    
    


    
    

    