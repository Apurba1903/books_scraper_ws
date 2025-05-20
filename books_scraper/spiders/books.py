import scrapy
from books_scraper.items import BookScraperItem


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
