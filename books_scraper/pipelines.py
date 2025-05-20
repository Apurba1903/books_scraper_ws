# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BooksScraperPipeline:
    def process_item(self, item, spider):
        return item


class booksPipeline:
    def process_item(self, item, spider):
        item['title'] = item['title'].strip() if item['title'] else None

        price = item.get('price', '').replace('£', '').replace('$', '').strip()
        try:
            item['price'] = float(price) if price else None
        except ValueError:
            item['price'] = None

        rating_val = item.get('rating', '')
        if rating_val:
            rating_word = rating_val.replace('star-rating', '').strip()
            rating_map = {
                'One': 1,
                'Two': 2,
                'Three': 3,
                'Four': 4,
                'Five': 5
            }
            item['rating'] = rating_map.get(rating_word, None)
        else:
            item['rating'] = None

        return item