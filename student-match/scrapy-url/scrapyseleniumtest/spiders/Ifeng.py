# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from bs4 import BeautifulSoup
from urllib.parse import quote
from scrapyseleniumtest.items import NewsItem


class IfengSpider(Spider):
    name = 'Ifeng'
    allowed_domains = ['//www.godasai.com/']

    def start_requests(self):
        url = 'http://www.godasai.com/'
        yield Request(url, self.parse)

    def parse(self, response):
        '''
        soup = BeautifulSoup(response.text,'lxml')
        urls = soup.find_all('div',class_='row')
        for urlitem in urls:
            item = NewsItem()
            item['url'] = urlitem.find('a', href=True)['href']
            yield item
        '''

        urls = response.xpath('/html/body/table[6]/tr/td[2]/table[3]/tr/td/ul/li')
        for urlitem in urls:
            item = NewsItem()
            item['url'] = urlitem.xpath('./a/@href').extract()[0]
            item['title'] = urlitem.xpath('./a/@title').extract()[0]
            item['date'] = urlitem.xpath('./a/@href').extract()[0].split('/')[-2]
            item['type'] = '艺术设计类'
            yield item

