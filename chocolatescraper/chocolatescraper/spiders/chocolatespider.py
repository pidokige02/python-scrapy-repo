import scrapy


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):

        products = response.css("product-item")
        for product in products:
            # data 추출하는 용도의 yield
            yield {
                "name": product.css("a.product-item-meta__title::text").get(),
                "price": product.css("span.price")
                .get()
                .replace(
                    '<span class="price price--highlight">\n              <span class="visually-hidden">Sale price</span>',
                    "",
                )
                .replace("</span>", ""),
                "url": product.css("div.product-item-meta a").attrib["href"],
            }

        next_page = response.css('[rel="next"]::attr(href)').get()

        if next_page is not None:
            next_page_url = "https://www.chocolate.co.uk" + next_page
            # 새로운 요청을 생성하고, 이를 Scrapy 엔진에 전달하여 다음 페이지를 크롤링
            yield response.follow(next_page_url, callback=self.parse)
