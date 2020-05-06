# -*- coding: utf-8 -*-
from scrapy import Request, Spider
import re
from lxml import etree
from scrapyseleniumtest.items import NewsItem

class IfengSpider(Spider):
    name = 'Ifeng'

    def start_requests(self):
        with open(r'C:\Users\SONY\Desktop\scrapy\studentmatchurl.csv', "r", encoding='UTF-8') as file:
            file_list = file.readlines()
            for eachone in file_list:
                url = eachone
                yield Request(url, self.parse)

    def parse(self, response):

        item = NewsItem()
        item['url'] = response.url
        content_list = response.xpath('//*[contains(@style,"word-break: break-all")]//text()').extract()
        strings = ''
        if content_list is []:
            content_list = response.xpath('//*[contains(@style,"text-indent: ")]//text()').extract()
        for content in content_list:
            str = content
            if len(str) <= 3:
                strings += str
            else:
                strings += str
                strings += '\n'

        item['page'] = strings.replace('\xa0','').replace('◎初赛名单◎初赛获奖名单◎复赛名单◎复赛获奖名单◎决赛名单◎决赛获奖名单\n', '').replace('去大赛网(www.godasai.com)提醒您：有更新后字体将变为蓝色，点击对应链接即可\n','').replace('&nbsp;','').replace('去大赛网（www.godasai.com）提醒您：\n','').replace('关注我们(微号：godasai)可获得更多最新可报名大学生竞赛赛事信息：\n','').replace('◎初赛名单\n','').replace('◎初赛获奖名单◎复赛名单◎复赛获奖名单◎决赛名单◎决赛获奖名单\n','').replace('去大赛网(\n','').replace('www.godasai.com)提醒您：有更新后字体将变为蓝色，点击对应链接即可\n','').replace('去大赛网\n','').replace('www.godasai.com)提醒您：有更新后字体将变为蓝色，点击对应链接即可\n','').replace('关注我们\n','').replace('(微号：godasai)可获得更多最新可报名大学生竞赛赛事信息：\n','')

        yield item





