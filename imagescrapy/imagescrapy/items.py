# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class ImageItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = table = 'images'
    id = Field()   #hbased的rowkey
    url = Field()  #图片链接
    filename = Field() #图片名
    status = Field()  #链接状态，已成功爬取为crawled，未爬取或未成功爬取为nocrawl
    flag = Field()   #下载状态，成功为ok，失败为fail
    hdfs = Field()   #HDFS上传状态，成功为ok，失败为fail
    pass

