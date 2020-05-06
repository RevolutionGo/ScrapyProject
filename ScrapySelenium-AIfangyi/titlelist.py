import json
import requests
import time
import random
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.aifangyi
collection = db.aifangyi
keyword = ['']
tlist = ['']
i = 0

baseurl = r'https://wenzhen.sogou.com/hospital/consultation/robot/listData?keyword='
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

while i < 100:
    time.sleep(1)
    url = baseurl + keyword[i]
    response = requests.get(url,headers= headers)
    time.sleep(1)
    i += 1
    s = json.loads(response.text)
    nexttitle = s["data"]["recommend"][random.randint(0,2)]["title"]
    print("nexttite = " + nexttitle)
    #if nexttitle not in keyword:
    keyword.append(nexttitle)


    for eachone in s["data"]["recommend"]:
        print("tite = " + eachone["title"])
        if eachone["title"] not in tlist:
            tlist.append(eachone["title"])
            post = eachone
            collection.insert_one(post)






