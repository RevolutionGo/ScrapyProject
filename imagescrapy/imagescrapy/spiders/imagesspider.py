# -*- coding: utf-8 -*-
import openpyxl
import re
from scrapy import Spider, Request
from imagescrapy.items import ImageItem

class ImagesspiderSpider(Spider):
    name = 'imagesspider'
    allowed_domains = ['hbimg.huabanimg.com']
    start_urls = ['http://hbimg.huabanimg.com/']

    def start_requests(self):
        #获取xlxs文件
        workbook = openpyxl.load_workbook(r'C:\Users\SONY\Desktop\scrapy\创新实践数据库.xlsx')
        #获取文件中的第一个表
        worksheet = workbook.worksheets[0]

        #获取第2行之后到MAX_IMAGES间第一列的数据
        for i in range(800, self.settings.get('MAX_IMAGES') + 2):
            for j in range(1, 2):
                link = worksheet.cell(row=i, column=j).value
                url = 'http:'+ re.sub(r'https:', "", link)
                id = i
                yield Request(url,meta={'id':id},callback=self.parse)

    def parse(self, response):
        url = response.request.url
        url = response.urljoin(url)
        item = ImageItem()
        item['id'] =  response.meta['id']
        item['url'] = url
        if response.status == 200:
            item['status'] = 'crawled'
        else:
            item['status'] = 'nocrawl'
        yield item
        pass
