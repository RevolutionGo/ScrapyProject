# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import pymongo
import pymysql
#import happybase
#from hashlib import md5
from scrapy import Request
import requests
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1] + '.png'
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        item['flag'] = 'ok'
        if not image_paths:
            item['flag'] = 'fail'
            #raise DropItem('Image Downloaded Failed')若下载失败则抛出异常，该item会被忽略
        return item

    def get_media_requests(self, item, info):
        yield Request(item['url'])


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.collection
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()


class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item

#以Rest API方式访问Hbase
class HbasePipeline():
    def __init__(self, baseurl):
        self.baseurl = baseurl

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            baseurl=crawler.settings.get('HBASE_BASEURL'),
        )

    def process_item(self, item, spider):
        dir = os.getcwd()  # 当前工作目录
        id = str(item['id'])
        url = item['url']
        item['filename'] = url.split('/')[-1] + '.png'
        filename = item['filename']
        status = item['status']
        flag = item['flag']
        item['hdfs'] = 'false'

        insert1 = '/hbase/insertRow?tableName=imagescrapy&familyName=image&rowKey='+ id
        insert2 = '&column=url&value='+ url
        insert3 = '&column=status&value='+ status
        insert4 = '&column=flag&value='+ flag
        insert5 = '&column=filename&value='+ filename
        insert6 = '&column=hdfs&value='
        uploadfile = '/api/hdfs/file/uplocalfile'

        requests.post(self.baseurl+ insert1+  insert2, headers={"Accept": "application/json"})
        requests.post(self.baseurl+ insert1+  insert3, headers={"Accept": "application/json"})
        requests.post(self.baseurl+ insert1+  insert4, headers={"Accept": "application/json"})
        requests.post(self.baseurl+ insert1+  insert5, headers={"Accept": "application/json"})

        imgpath = dir + '\\images\\' +filename
        files = {'file': (filename, open(imgpath, 'rb'), 'application/octet-stream', {})}
        response = requests.request("post", self.baseurl+ uploadfile, files=files)
        if response.json()["code"] == "200":
            item['hdfs'] = 'ok'
            print(response.json())

        hdfs = item['hdfs']
        requests.post(self.baseurl + insert1 + insert6 + hdfs, headers={"Accept": "application/json"})
        return item


'''
利用thrift服务和happybase库连接hbase
class HbasePipeline(object):
    def __init__(self, host, table_name):
        self.host = host
        self.table_name = table_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('HBASE_HOST'),
            table_name=crawler.settings.get('HBASE_TABLE'),
        )

    def open_spider(self, spider):
        self.connection = happybase.Connection(self.host)
        table = self.connection.table(self.table_name)
        self.table = table

    def process_item(self, item, spider):
        url = item['url']
        flag = item['flag']
        #对url进行哈希，返回十六进制（通过哈希值建立索引，提高数据库的响应速度）
        self.table.put(md5(url).hexdigest(),{'cf1:url':url,'cf1:flag':flag})
        return item
'''