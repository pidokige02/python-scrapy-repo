# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item

class PriceToUSDPipeline:
    gbpToUsdRRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):

            float_price = float(adapter['price'])

            adapter['price'] = float_price * self.gbpToUsdRRate

            return item

        else:
            raise DropItem("Missing price in {item}")


class DuplicatePipeline:

    def __init__(self):
        self.name_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('name') in self.name_seen:
            raise DropItem("Duplicate item found : {item!r}")
        else:
            self.name_seen.add(adapter['name'])
            return item