# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urllib.parse import quote
from bs4 import BeautifulSoup
from scrapysplashtest.items import NewsItem
from scrapy_splash import SplashRequest

script1 = """
function main(splash, args)
  splash.images_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(args.wait))
  return splash:html()
end
"""

script2 = """
function main(splash, args)
  splash.images_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(args.wait))
  splash:evaljs('document.querySelector(".menu-item user_votes").click()')
  return splash:html()
end
"""

class IfengSpider(Spider):
    name = 'Ifeng'
    allowed_domains = ['//www.awwwards.com/']
    baseurl = 'https://www.awwwards.com'
    
    def start_requests(self):
        with open(r'C:\Users\SONY\Desktop\scrapy\awwwardsurl.txt', "r", encoding='UTF-8') as file:
            file_list = file.readlines()
            for eachone in file_list:
                link = eachone.strip()
                url = self.baseurl + link
                yield SplashRequest(url, callback=self.parse, endpoint='execute',
                              args={'lua_source': script1, 'wait': 7})
    
    def parse(self, response):
        item = NewsItem()
        soup = BeautifulSoup(response.text, 'html.parser')
        item['url'] = response.request.url
        item['design'] = soup.find('li', class_='circle-note-progress style-design').get('data-note')
        item['usability'] = soup.find('li', class_='circle-note-progress style-usability').get('data-note')
        item['creativity'] = soup.find('li', class_='circle-note-progress style-creativity').get('data-note')
        item['content'] = soup.find('li', class_='circle-note-progress style-content').get('data-note')
        item['mobile'] = soup.find('li', class_='circle-note-progress style-mobile').get('data-note')
        item['developer'] = soup.find('li', class_='circle-note-progress style-developer').get('data-note')

        item['screenshots1'] = response.xpath('//*[@id="screenshots"]/div/div[1]/div/a/img/@data-src').extract()[0]
        item['screenshots2'] = response.xpath('//*[@id="screenshots"]/div/div[2]/div/a/img/@data-src').extract()[0]

        v1 = response.xpath(
            '//*[@id="content"]/div/div[3]/div/div[2]/div/ul/li[1]/div/figure/a/span/video/source/@data-src').extract()
        v2 = response.xpath(
            '//*[@id="content"]/div/div[3]/div/div[2]/div/ul/li[2]/div/figure/a/span/video/source/@data-src').extract()

        if v1 == []:
            item['video1'] = ''
        else:
            item['video1'] = response.xpath('//*[@id="content"]/div/div[3]/div/div[2]/div/ul/li[1]/div/figure/a/span/video/source/@data-src').extract()[0]

        if v2 == []:
            item['video2'] = ''
        else:
            item['video2'] = response.xpath('//*[@id="content"]/div/div[3]/div/div[2]/div/ul/li[2]/div/figure/a/span/video/source/@data-src').extract()[0]

        judges = response.xpath('//*[@id="jury_votes"]/li')
        judgelist = []

        for j in judges:
            usrid = j.xpath('./div[1]/div[2]//div/div[1]/strong[1]/a/text()').extract()
            fro = j.xpath('./div[1]/div[2]/div/div[1]/strong[2]/text()').extract()
            design = j.xpath('./div[2]/ul[1]/li[1]/@data-note').extract()
            usability = j.xpath('./div[2]/ul[1]/li[2]/@data-note').extract()
            creativity = j.xpath('./div[2]/ul[1]/li[3]/@data-note').extract()
            content = j.xpath('./div[2]/ul[1]/li[4]/@data-note').extract()
            avrage = j.xpath('./div[2]/div/span/text()').extract()

            if usrid == []:
                usrid_ = ''
            else:
                usrid_ = j.xpath('./div[1]/div[2]//div/div[1]/strong[1]/a/text()').extract()[0]
            if fro == []:
                from_ = ''
            else:
                from_ = j.xpath('./div[1]/div[2]/div/div[1]/strong[2]/text()').extract()[0]
            if design == []:
                design_ = ''
            else:
                design_ = j.xpath('./div[2]/ul[1]/li[1]/@data-note').extract()[0]
            if usability == []:
                usability_ = ''
            else:
                usability_ = j.xpath('./div[2]/ul[1]/li[2]/@data-note').extract()[0]
            if creativity == []:
                creativity_ = ''
            else:
                creativity_ = j.xpath('./div[2]/ul[1]/li[3]/@data-note').extract()[0]
            if content == []:
                content_ = ''
            else:
                content_ = j.xpath('./div[2]/ul[1]/li[4]/@data-note').extract()[0]
            if avrage == []:
                avrage_ = ''
            else:
                avrage_ = j.xpath('./div[2]/div/span/text()').extract()[0]

            judge = {
                "usrid": usrid_,
                "from": from_,
                "design": design_,
                "usability": usability_,
                "creativity": creativity_,
                "content": content_,
                "avrage": avrage_,
            }
            judgelist.append(judge)

        item['judges'] = judgelist
        yield SplashRequest(url=item['url'], meta={'item': item},callback=self.parse_detailsinfo,endpoint='execute',
                      args={'lua_source': script2, 'wait': 3})

    def parse_detailsinfo(self, response):
        # 通过response.meta['item']获取参数
        item = response.meta['item']
        users = response.xpath('//*[@id="user_votes"]/li')
        userslist = []
        for u in users:
            uusrid = u.xpath('./div[1]/div[2]//div/div[1]/strong[1]/a/text()').extract()
            ufro = u.xpath('./div[1]/div[2]/div/div[1]/strong[2]/text()').extract()
            udesign = u.xpath('./div[2]/ul[1]/li[1]/@data-note').extract()
            uusability = u.xpath('./div[2]/ul[1]/li[2]/@data-note').extract()
            ucreativity =  u.xpath('./div[2]/ul[1]/li[3]/@data-note').extract()
            ucontent = u.xpath('./div[2]/ul[1]/li[4]/@data-note').extract()
            uavrage =  u.xpath('./div[2]/div/span/text()').extract()

            if uusrid == []:
                uusrid_ = ''
            else:
                uusrid_ = u.xpath('./div[1]/div[2]//div/div[1]/strong[1]/a/text()').extract()[0]
            if ufro == []:
                ufrom_ = ''
            else:
                ufrom_ = u.xpath('./div[1]/div[2]/div/div[1]/strong[2]/text()').extract()[0]
            if udesign == []:
                udesign_ = ''
            else:
                udesign_ = u.xpath('./div[2]/ul[1]/li[1]/@data-note').extract()[0]
            if uusability == []:
                uusability_ = ''
            else:
                uusability_ = u.xpath('./div[2]/ul[1]/li[2]/@data-note').extract()[0]
            if ucreativity == []:
                ucreativity_ = ''
            else:
                ucreativity_ =  u.xpath('./div[2]/ul[1]/li[3]/@data-note').extract()[0]
            if ucontent == []:
                ucontent_ = ''
            else:
                ucontent_ = u.xpath('./div[2]/ul[1]/li[4]/@data-note').extract()[0]
            if uavrage == []:
                uavrage_ = ''
            else:
                uavrage_ = u.xpath('./div[2]/div/span/text()').extract()[0]

            user = {
                "usrid": uusrid_,
                "from": ufrom_,
                "design": udesign_,
                "usability": uusability_,
                "creativity": ucreativity_,
                "content": ucontent_,
                "avrage": uavrage_,
            }
            userslist.append(user)

        item['users'] = userslist

        yield item