# Samsung Price Monitor
---
### Description
Samsung Price Monitor is a Python application that regularly scrapes Samsung product listings from their [Official Jumia store](https://www.jumia.co.ke/mlp-samsung-shop/), monitors their prices, and sends email notifications when discounts are detected.

---
### Features
+ Automated web scraping of Samsung products from their official Jumia store
+ Regular price checks and comparison with previous data
+ Email notifications for price drops and discounts
+ Customizable monitoring frequency and discount thresholds

---
### Installation
1. Clone this repository:

```
https://github.com/daniel-ndirangu/Jumia-Price-Tracker.git
```

2. Navigate to the project directory:

```
cd jumiascraper
```

3. Install required dependencies:
```
pip install -r requirements.txt
```

---

### Dependencies

+ Python 3.10+

+ Scrapy 

+ Scrapy-playwright

+ Prefect

---

### Setting Up Automation
---
Prefect, a work orchestration tool, was utilized to automate and schedule the collection of prices
