import scrapy
from quotes_js_scraper.items import QuoteItem
from scrapy_playwright.page import PageMethod

# codes for "Scraping Multiple Pages"
# class QuotesSpider(scrapy.Spider):
#     name = 'quotes'
#     # allowed_domains = ['quotes.toscrape.com']
#     # start_urls = ['http://quotes.toscrape.com/']


#     def start_requests(self):
#         url = 'https://quotes.toscrape.com/js/'
#         yield scrapy.Request(url, meta=dict(
# 			playwright = True,
# 			playwright_include_page = True,
#             playwright_page_methods =[PageMethod('wait_for_selector', 'div.quote')],
#                     errback=self.errback,
# 		))

#     async def parse(self, response):
#         page = response.meta["playwright_page"]
#         await page.close()

#         for quote in response.css('div.quote'):
#             quote_item = QuoteItem()
#             quote_item['text'] = quote.css('span.text::text').get()
#             quote_item['author'] = quote.css('small.author::text').get()
#             quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
#             yield quote_item

#         next_page = response.css('.next>a ::attr(href)').get()

#         if next_page is not None:
#             next_page_url = 'http://quotes.toscrape.com' + next_page
#             yield scrapy.Request(next_page_url, meta=dict(
#                 playwright = True,
#                 playwright_include_page = True,
#                 playwright_page_methods =[
#                     PageMethod('wait_for_selector', 'div.quote'),
#                 ],
#                 errback=self.errback,
#             ))

#     async def errback(self, failure):
#         page = failure.request.meta["playwright_page"]
#         await page.close()

# codes for "Scroll Down Infinite Scroll Pages"
class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        url = "https://quotes.toscrape.com/scroll"
        yield scrapy.Request(url, meta=dict(
				playwright = True,
				playwright_include_page = True,
				playwright_page_methods =[
          PageMethod("wait_for_selector", "div.quote"),
          PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
          PageMethod("wait_for_selector", "div.quote:nth-child(11)"),  # 10 per page
          ],
        errback=self.errback,
			))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
