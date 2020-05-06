# -*- coding: utf-8 -*-
from scrapy import Request, Spider
import json
from urllib.parse import quote
from scrapyseleniumtest.items import NewsItem

class IfengSpider(Spider):
    name = 'Ifeng'
    allowed_domains = ['//wenzhen.sogou.com/hospital/consultation/robot/']
    start_urls = ['https://wenzhen.sogou.com/hospital/consultation/robot/listData?keyword=']

    def start_requests(self):
        baseurl = 'https://wenzhen.sogou.com/hospital/consultation/robot/listData?keyword='
        with open(r'C:\Users\SONY\Desktop\scrapy\keyword.csv', "r", encoding='UTF-8') as file:
            file_list = file.readlines()
            for eachone in file_list:
                link = eachone
                url = baseurl + link
                yield Request(url, self.parse)

    def parse(self,response):
        item = NewsItem()
        jsonresponse = json.loads(response.text, strict=False)
        item['title'] = jsonresponse["data"]["QA"]["title"]
        item['answer'] = jsonresponse["data"]["QA"]["answer"]
        item['id'] = jsonresponse["data"]["QA"]["id"]
        yield item




