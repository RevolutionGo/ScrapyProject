# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class NewsItem(Item):
    collection = table = 'studentmatch'
    url = Field()
    page = Field()



