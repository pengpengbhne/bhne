# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dongguan.items import DongguanItem


class SunSpider(CrawlSpider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://d.wz.sun0769.com/index.php/question/huiyin?type=4&page=0']

    rules = (
        Rule(LinkExtractor(allow=r'type=4&page=\d+'), process_links="deal_links", follow=True),
        Rule(LinkExtractor(allow=r'/html/question/\d+/\d+.shtml'), callback='parse_item', follow=False),
    )

    def deal_link(self, links):
        for link in links:
            link.url = link.url.replace("&", "?").replace("Type&", "Type?")
        return links

    def parse_item(self, response):
       item = DongguanItem()
       # 标题
       item['title'] = response.xpath('//div[contains(@class, "pagecenter p3")]//strong/text()').extract()[0]
       # 编号
       item['number'] = item['title'].split(' ')[-1].split(":")[-1]
       # 内容
       item['content'] = response.xpath('//div[@class="c1 text14_2"]/text()').extract()[0]
       # 链接
       item['url'] = response.url

       yield item
