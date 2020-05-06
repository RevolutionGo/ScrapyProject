# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from awwwards.items import AwwwardsItem

class AwwwardsSpider(Spider):
    name = 'awwwards'
    #allowed_domains = ['//www.awwwards.com']
    baseurl = 'https://www.awwwards.com'

    def start_requests(self):
        with open(r'C:\Users\SONY\Desktop\scrapy\awwwardsurl.txt', "r", encoding='UTF-8') as file:
            file_list = file.readlines()
            for eachone in file_list:
                link = eachone
                url = self.baseurl + link
                yield Request(url, self.parse)

    def parse(self, response):
        item = AwwwardsItem()
        item['url'] = response.request.url
        yield item

