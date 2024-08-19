import scrapy
from jumiascraper.items import JumiascraperItem
from scrapy.loader import ItemLoader


class SamsungSpider(scrapy.Spider):
    
    name = "products"
    
    allowed_domains = ["www.jumia.co.ke"]
    
    start_urls = ["https://www.jumia.co.ke/mlp-samsung-shop/"]

    def parse(self, response):
        
        for product in response.css("article.prd._fb.col.c-prd"):
            
            item = ItemLoader(item=JumiascraperItem(), selector=product)
            
            item.add_css("product", "h3.name::text") # product name
            
            item.add_css("current_price", "div.prc::text") # current price
            
            item.add_css("original_price", "div.old::text") # Original price
            
            item.add_css("store_discount", "div.bdg._dsct._sm::text") # Discounts
            
            # item.add_css("url", "a.core::attr(href)")
            
            product_link = product.css("a.core::attr(href)").get() 
            
            url = response.urljoin(product_link)
            
            yield scrapy.Request(url=url, callback=self.parse_description, meta={"item": item})
            
    def parse_description(self, response):
        
        item = response.meta["item"]
        item.selector = response
        
        item.add_css("store", "a.bdg._mall._sm.-mrs::text")
        item.add_css("brand", "div.-pvxs a:nth-child(1)::text")
        
        yield  item.load_item()
