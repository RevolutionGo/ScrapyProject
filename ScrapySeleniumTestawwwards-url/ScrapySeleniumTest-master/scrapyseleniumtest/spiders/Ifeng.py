# -*- coding: utf-8 -*-
from scrapy import Request, Spider
from bs4 import BeautifulSoup
from urllib.parse import quote
from scrapyseleniumtest.items import NewsItem


class IfengSpider(Spider):
    name = 'Ifeng'
    allowed_domains = ['//www.awwwards.com/websites/']
    base_urls = 'https://www.awwwards.com/websites/sites_of_the_day/?page='

    def start_requests(self):
            for page in range(1,11):
                url = self.base_urls + str(page) + ".html"
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
        urls = response.xpath('//*[@class="list-items list-flex js-elements-container"]/li')
        for urlitem in urls:
            item = NewsItem()
            item['url'] = urlitem.xpath('./div/div/div[1]/div[1]/h3/a/@href').extract()[0]
            yield item

