import scrapy
from books_scraper.items import BookScraperItem
from scrapy.exceptions import CloseSpider
from urllib.parse import urljoin


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        for book in response.css('article.product_pod'):
            item = BookScraperItem()
            item['title'] = book.css('h3 a::attr(title)').get()
            item['price'] = book.css('p.price_color::text').get()
            item['rating'] = book.css('p.star-rating::attr(class)').get()
            
            yield item

        try:
            next_page = response.css('li.next a::attr(href)').get()
            if next_page:
                next_page_url = urljoin(response.url, next_page)
                yield scrapy.Request(next_page_url, callback=self.parse)
        except Exception as e:
            self.logger.error(f"Pagination error: {e}")
            raise CloseSpider('Pagination failed')