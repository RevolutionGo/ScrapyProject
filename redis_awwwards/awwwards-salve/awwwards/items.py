# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class AwwwardsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = table = 'redisawwwards'

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

