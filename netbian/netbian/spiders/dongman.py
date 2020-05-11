# -*- coding: utf-8 -*-
import scrapy
from ..items import NetbianItem


class DongmanSpider(scrapy.Spider):
    name = 'dongman'
    allowed_domains = ['pic.netbian.com']
    start_urls = ['http://pic.netbian.com/4kdongman/']
    host_url = 'http://pic.netbian.com'

    def parse(self, response):
        img_list = response.xpath('//ul[@class="clearfix"]/li')
        for img in img_list:
            info_url = self.host_url + img.xpath('./a/@href').get()
            yield scrapy.Request(info_url, self.parse_info)

        page_urls = response.xpath('//div[@class="page"]/a')
        next_page = [p.xpath('./@href').get() for p in page_urls if p.xpath('./text()').get() == '下一页'][0]
        if next_page:
            yield response.follow(self.host_url + next_page, self.parse)

    def parse_info(self, response):
        item = NetbianItem()
        item['image_urls'] = self.host_url + response.xpath('//a[@id="img"]/img/@src').get()
        item['names'] = response.xpath('//a[@id="img"]/img/@title').get()
        yield item