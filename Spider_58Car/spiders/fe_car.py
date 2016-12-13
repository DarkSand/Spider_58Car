# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Spider_58Car.items import FeCarItem
import sys
import time
import re
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')


class FeCarSpider(scrapy.Spider):
    name = "Spider_58Car"
    allowed_domains = ["58.com"]
    start_urls = (
        'http://www.58.com/maiche/changecity/',
    )

    def parse(self, response):
        if 'changecity' in response.request.url:
            clist = response.css('dl#clist a')
            for city in clist:
                url = city.css('::attr(href)').extract_first()
                cityname = city.css('::text').extract_first()
                if 'maiche' in url:
                    request = Request(
                            url=url,
                            dont_filter=True
                    )
                    request.meta['city'] = cityname
                    yield request
                    time.sleep(0.2)
        elif response.request.meta.has_key('pagesrc'):
            mobile = response.css('span.l_phone::text').extract_first()
            if mobile is not None:
                try:
                    item = FeCarItem()
                    item['mobile'] = mobile.strip()
                    item['title'] = string_formart(response.css('h1::text').extract_first().strip())
                    item['contact_man'] = string_formart(response.xpath(
                        u'//div[contains(text(),\'联系人\')]/following-sibling::*[1]/a/text()').extract_first())
                    if item['contact_man'] is None:
                        item['contact_man'] = string_formart(response.xpath(
                            u'//div[contains(text(),\'联\') and contains(text(),\'系\') and contains(text(),\'人\')]/following-sibling::*[1]/a/text()').extract_first())
                    item['url'] = response.request.url
                    item['city'] = response.request.meta['city']
                    item['company_name'] = response.css('div.userinfo h2::text').extract_first().replace(' ',
                                                                                                         '').replace(
                        '\r', '').replace('\n', '').replace('\t', '') if response.css(
                        'div.userinfo h2::text').extract_first() is not None else None
                    item['gather_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    item['timeSpan'] = str(time.time())
                    yield item
                except:
                    print 'error:' + traceback.format_exc() + '\n' + 'url:' + response.request.url
        else:
            next_page = response.css('a.next::attr(href)').extract_first()
            if next_page:
                domain = re.search(".*?.com", response.request.url).group()
                request = Request(
                        url=domain + next_page,
                        dont_filter=True
                )
                request.meta['city'] = response.request.meta['city']
                yield request
            loan_list = response.css('a.t::attr(href)').extract()
            for loan in loan_list:
                request = Request(
                        url=loan,
                        dont_filter=True,
                )
                request.meta['pagesrc'] = 'True'
                request.meta['city'] = response.request.meta['city']
                yield request


def string_formart(m_str):
    if m_str is not None:
        return m_str.replace(' ', '').replace('\r', '').replace('\n', '').replace('\t', '')
    else:
        return m_str
