# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


class NewsItem(Item):
    collection = table = 'awwwards'

    url = Field()
    design = Field()
    usability = Field()
    creativity = Field()
    content = Field()
    mobile = Field()
    developer = Field()
    screenshots1 = Field()
    screenshots2 = Field()
    video1 = Field()
    video2 = Field()
    judges = Field()
    users = Field()