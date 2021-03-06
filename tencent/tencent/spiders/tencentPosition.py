# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem


class TencentpositionSpider(scrapy.Spider):
    name = 'tencentPosition'
    allowed_domains = ['tencent.com']
    url = 'http://hr.tencent.com/position.php?&start='
    offset = 0
    start_urls = [url + str(offset)]
    # http://wz.sun0769.com/index.php/question/huiyin?type=4&page=30
    def parse(self, response):
        for each in response.xpath('//tr[@class="even"] | //tr[@class="odd"]'):
            # 初始化对象
            item = TencentItem()
            # 职位名称
            item['name'] = each.xpath("./td[1]/a/text()").extract()[0]
            # 详情链接
            item['link'] = each.xpath("./td[1]/a/@href").extract()[0]
            # 职位类别
            item['positionType'] = each.xpath("./td[2]/text()").extract()[0]
            # 招聘人数
            item['peopleNum'] = each.xpath("./td[3]/text()").extract()[0]
            # 工作地点
            item['workLocation'] = each.xpath("./td[4]/text()").extract()[0]
            # 发布时间
            item['publishTime'] = each.xpath("./td[5]/text()").extract()[0]

            yield item

        if self.offset < 1000:
            self.offset += 10

        # 将请求重新发送
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

