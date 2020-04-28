# -*- coding: utf-8 -*-
import scrapy

from ..items import NetbianItem


class FourSpider(scrapy.Spider):
    name = 'four'
    allowed_domains = ['pic.netbian.com']
    start_urls = ['http://pic.netbian.com/']

    def parse(self, response):
        item = NetbianItem()
        urls = response.xpath('//div[@class="slist"]/ul/li/a/span/img')
        # for url in urls:
        #     yield {
        #         'src': self.start_urls[0] + url.xpath('./@src').extract_first(),
        #         'alt': url.xpath('./@alt').extract_first()
        #     }
        src_list = []
        alt_list = []
        for url in urls:
            src_list.append(self.start_urls[0] + url.xpath('./@src').extract_first())
            alt_list.append(url.xpath('./@alt').extract_first())
        item['image_urls'] = src_list
        item['names'] = alt_list
        yield item
