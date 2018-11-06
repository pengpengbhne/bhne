# -*- coding: utf-8 -*-
import scrapy
import json
from douyu.items import DouyuItem


class DouyumeinvSpider(scrapy.Spider):
    name = 'douyumeinv'
    allowed_domains = ['capi.douyucdn.cn']
    offset = 0
    url = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="

    start_urls = [url + str(offset)]

    def parse(self, response):
        data = json.loads(response.text)['data']
        for each in data:
            item = DouyuItem()
            item['name'] = each['nickname']
            item['imglink'] = each['vertical_src']
            yield item

        self.offset += 20
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

