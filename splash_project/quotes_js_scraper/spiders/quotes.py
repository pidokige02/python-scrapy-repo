import scrapy
import base64
from quotes_js_scraper.items import QuoteItem
from scrapy_splash import SplashRequest

javascript_script = """
element = document.querySelector('h1').innerHTML = 'The best quotes of all time!'
"""
class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        url = 'https://quotes.toscrape.com/js/'
        yield SplashRequest(
            url,
            callback=self.parse,
            endpoint='render.json',
            args={
                'wait': 2,
                'js_source': javascript_script,
                'html': 1,
                'png': 1,
                'width': 1000,
            })
        
    def parse(self, response):
        imgdata = base64.b64decode(response.data['png'])
        filename = 'some_image.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)