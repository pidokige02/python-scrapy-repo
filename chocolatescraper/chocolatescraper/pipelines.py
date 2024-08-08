# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from mysql.connector import Error
import psycopg2

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


class SavingToMysqlPipeline(object):

    def __init__(self):
       self.create_connection()

    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host = 'localhost',
                user = 'pidokige',
                password = 'Feb02pid~',
                database = 'scraping',
                port = '3306'
            )
            self.curr = self.connection.cursor()
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        adapter = ItemAdapter(item)
        try:
            self.curr.execute(
                """INSERT INTO chocolate_products (name, price, url) VALUES (%s, %s, %s )""",
                (
                    adapter.get("name"),
                    adapter.get("price"),
                    adapter.get("url")
                )
            )
            self.connection.commit()
        except Error as e:
            print(f"Error while inserting to MySQL: {e}")

class SavingToPostgresPipeline(object):

    def __init__(self):
       self.create_connection()

    def create_connection(self):
        try:
            self.connection = psycopg2.connect(
                host = 'localhost',
                user = 'root',
                password = 'secret123',
                database = 'scraping',
            )
            self.curr = self.connection.cursor()
        except Error as e:
            print(f"Error while connecting to PostgreSQL: {e}")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        adapter = ItemAdapter(item)
        try:
            self.curr.execute(
                """INSERT INTO chocolate_products (name, price, url) VALUES (%s, %s, %s )""",
                (
                    adapter.get("name"),
                    adapter.get("price"),
                    adapter.get("url")
                )
            )
            self.connection.commit()
        except Error as e:
            print(f"Error while inserting to PostgreSQL: {e}")