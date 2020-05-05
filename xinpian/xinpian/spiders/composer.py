# -*- coding: utf-8 -*-
import random
import string

import scrapy

from ..items import ComposerItem

cookies = {
    'Authorization': 'D6FCBCCA2638248E62638245E5263829C1126382B1EDFA613BB7'
}


def gen_session_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=26))


class ComposerSpider(scrapy.Spider):
    name = 'composer'
    allowed_domains = ['www.xinpianchang.com']
    start_urls = ['https://www.xinpianchang.com/user/stars?from=navigator']
    page_count = 0

    def parse(self, response):
        # 创作人详情
        user_url_list = response.xpath('//div[@class="info-con"]/a/@href').extract()
        for user_url in user_url_list:
            yield response.follow('https://www.xinpianchang.com' + user_url, self.parse_user_info)

        # PHPSESSID
        self.page_count += 1
        if self.page_count >= 50:
            self.page_count = 0
            cookies.update(PHPSESSID=gen_session_id())

        # 翻页
        next_page = response.xpath('//a[@title="下一页"]/@href').get()
        if next_page:
            next_page_url = 'https://www.xinpianchang.com' + next_page
            yield response.follow(next_page_url, self.parse, cookies=cookies)

    def parse_user_info(self, response):
        # 创始人信息
        item = ComposerItem()
        item['banner'] = response.xpath('//span[@class="avator-wrap-s"]/img/@src').get()
        item['nickname'] = response.xpath('//p[contains(@class, "creator-name")]/text()').get().strip()
        item['description'] = response.xpath('//p[contains(@class, "creator-desc")]/text()').get()
        item['like_counts'] = int(response.xpath('//span[contains(@class, "like-counts")]/text()').get().replace(',', ''))
        item['fans_counts'] = int(response.xpath('//span[contains(@class, "fans-counts")]/text()').get().replace(',', ''))
        item['concern'] = int(response.xpath('//span[@class="fw_600 v-center"]/text()').get().replace(',', ''))
        item['location'] = response.xpath('//span[@class="v-center"]/text()').extract()[-2]
        item['profession'] = response.xpath('//span[@class="v-center"]/text()').extract()[-1]
        yield item
