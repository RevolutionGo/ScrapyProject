# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from urllib.parse import quote
from scrapyseleniumtest.items import NewsItem


class IfengSpider(Spider):
    name = 'Ifeng'
    allowed_domains = ['www.news.ifeng.com']
    start_urls = ['https://news.ifeng.com/']


    def start_requests(self):
        with open(r'C:\Users\SONY\Desktop\scrapy\news_ifeng.txt', "r", encoding='UTF-8') as file:
            file_list = file.readlines()
            for eachone in file_list:
                link = eachone.strip()
                url = link
                yield Request(url, self.parse)

    def parse(self, response):
        url = response.request.url
        url = response.urljoin(url)
        page = response.text
        item = NewsItem()
        item['url'] = url
        item['page'] = page
        yield item


