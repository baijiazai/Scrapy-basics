# -*- coding: utf-8 -*-
import scrapy


class UsnewsSpider(scrapy.Spider):
    name = 'usnews'
    allowed_domains = ['qianmu.iguye.com']
    start_urls = [
        'http://www.qianmu.org/2020USNEWS%E7%BE%8E%E5%9B%BD%E7%BB%BC%E5%90%88%E6%80%A7%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D']

    def parse(self, response):
        keys = ['ranking', 'c_name', 'e_name', 'city', 'tuition', 'number', 'sat_avg', 'atc_avg']
        tr_list = response.xpath('//tbody/tr')
        for i in range(1, len(tr_list)):
            values = []
            td_list = tr_list[i].xpath('./td')
            for td in td_list:
                if td.xpath('./a/text()').extract_first() is None:
                    values.append(td.xpath('./text()').extract_first())
                else:
                    values.append(td.xpath('./a/text()').extract_first())
            data = {}
            for k, v in zip(keys, values):
                data[k] = v
            yield data
