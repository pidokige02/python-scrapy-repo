import scrapy
from chocolatescraper.items import ChocolateProduct
from chocolatescraper.itemloaders import ChocoloteProductLoader


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):

        products = response.css("product-item")

        for product in products:

            chocolate = ChocoloteProductLoader(
                item=ChocolateProduct(), selector=product
            )

            chocolate.add_css("name", "a.product-item-meta__title::text")
            chocolate.add_css(
                "price",
                "span.price",
                re='<span class="price price--highlight">\n              <span class="visually-hidden">Sale price</span>(.*)</span>',
            )
            chocolate.add_css("url", "div.product-item-meta a::attr(href)")
            # data 추출하는 용도의 yield
            yield chocolate.load_item()

        next_page = response.css('[rel="next"]::attr(href)').get()

        if next_page is not None:
            next_page_url = "https://www.chocolate.co.uk" + next_page
            # 새로운 요청을 생성하고, 이를 Scrapy 엔진에 전달하여 다음 페이지를 크롤링
            yield response.follow(next_page_url, callback=self.parse)
