import json
import requests
from selenium import webdriver

from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.awwwards
collection = db.first_mark

baseurl = r'https://www.awwwards.com/sites/elias-akentour-portfolio'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

# 启动浏览器，获取网页源代码
browser = webdriver.PhantomJS(r'C:\Users\SONY\AppData\Local\Programs\Python\Python36-32\Scripts\phantomjs.exe')

browser.get(baseurl)
b2 = r'//div[@class="box-notesite js-notes"]/ul/li[1]/div[@class="legend"]'
t1 = browser.find_element_by_xpath(b2).text
text = browser.find_element_by_xpath("//*[@id='content']/div/div[1]/div[3]/div[3]/div[1]/div[3]/ul/li[1]/div[2]").text
if t1 == "":
    print("text is null")
else:
    print(t1)
resonpse = browser.page_source #获取网页源码
#print(resonpse)
#保存网页源码
f = open(r'./page.html',mode='w',encoding='utf-8')
f.write(resonpse)


basexpath = r'//*[@id="content"]/div/div[1]/div[3]/div[3]/div[1]/div[3]/ul/li['

'''
for t in range(1,7):
    title = browser.find_element_by_xpath(basexpath + str(t) + r']/div[2]').text
    mardint = browser.find_element_by_xpath(basexpath + str(t) + r']/div[1]/div/span[1]').text
    mardpoint = browser.find_element_by_xpath(basexpath + str(t) + r']/div[1]/div/span[2]').text
    post = {
        "title": title,
        "mard": mardint + mardpoint
    }
    collection.insert_one(post)
'''
browser.quit()
