# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from bs4 import BeautifulSoup
from urllib.parse import quote
from scrapyseleniumtest.items import NewsItem


class IfengSpider(Spider):
    name = 'Ifeng'
    allowed_domains = ['www.china.chinadaily.com.cn']
    base_urls = 'https://china.chinadaily.com.cn/5bd5639ca3101a87ca8ff636/page_'

    def start_requests(self):
            for page in range(1,11):
                url = self.base_urls + str(page) + ".html"
                yield Request(url, self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text,'lxml')
        urls = soup.find_all('div',class_='mr10')
        for urlitem in urls:
            item = NewsItem()
            item['url'] = urlitem.find('a', href=True)['href']
            yield item


