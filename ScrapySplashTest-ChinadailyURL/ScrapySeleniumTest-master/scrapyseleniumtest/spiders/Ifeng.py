# -*- coding: utf-8 -*-
from scrapy import Request, Spider
import openpyxl
from urllib.parse import quote
from scrapyseleniumtest.items import NewsItem

class IfengSpider(Spider):
    name = 'Ifeng'
    allowed_domains = ['//china.chinadaily.com.cn/']
    start_urls = ['https://china.chinadaily.com.cn/']

    def start_requests(self):

        # 获取xlxs文件
        workbook = openpyxl.load_workbook(r'C:\Users\SONY\Desktop\scrapy\newsurl.xlsx')
        # 获取文件中的第一个表
        worksheet = workbook.worksheets[0]

        # 获取第2行之后到MAX_IMAGES间第一列的数据
        for i in range(2,3):
            for j in range(2, 3):
                link = worksheet.cell(row=i, column=j).value
                url = 'https:' + link
                yield Request(url,callback=self.parse)


    def parse(self, response):
        url = response.request.url
        url = response.urljoin(url)
        item = NewsItem()
        item['url'] = url
        item['page'] = response.text.replace("\n","").replace("\t","").replace(" ","")
        yield item


