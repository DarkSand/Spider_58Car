# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FeCarItem(scrapy.Item):
    mobile = scrapy.Field()
    title = scrapy.Field()
    contact_man = scrapy.Field()
    url = scrapy.Field()
    city = scrapy.Field()
    company_name = scrapy.Field()
    gather_time = scrapy.Field()
    timeSpan = scrapy.Field()
