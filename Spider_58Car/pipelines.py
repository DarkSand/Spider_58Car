# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class FeCarPipeline(object):
    def process_item(self, item, spider):
        return item


class ConsolePipeline(object):
    def process_item(self, item, spider):
        print json.dumps(dict(item)).decode('unicode-escape')
        return item


class TextPipline(object):
    def process_item(self, item, spider):
        with open('data.txt', 'a') as f:
            f.write(item['mobile'] + ',' +
                    item['city'] + ',' +
                    item['contact_man'] + ',' +
                    item['company_name'] + ',' +
                    item['gather_time'] + ',' +
                    item['title'] + ',' +
                    item['url'] + '\n')
        return item
