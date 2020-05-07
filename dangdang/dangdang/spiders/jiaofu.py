# -*- coding: utf-8 -*-
import random
import json

import scrapy
from scrapy.selector import Selector
from scrapy import Request
from ..items import BookInfoItem


class TongshuSpider(scrapy.Spider):
    name = 'jiaofu'
    allowed_domains = ['category.dangdang.com', 'product.dangdang.com']
    start_urls = [
        'http://category.dangdang.com/cp01.54.07.00.00.00.html',
        'http://category.dangdang.com/cp01.54.05.00.00.00.html',
        'http://category.dangdang.com/cp01.54.92.00.00.00.html',
        'http://category.dangdang.com/cp01.54.03.00.00.00.html',
        'http://category.dangdang.com/cp01.54.26.00.00.00.html'
    ]

    def parse(self, response):
        big_class = '教辅'
        small_class_old = response.xpath('/html/head/title/text()').get()
        small_class = small_class_old[:small_class_old.find('_')]

        book_list = response.xpath('//ul[@class="bigimg"]/li')
        for book in book_list:
            item = BookInfoItem()
            pid = book.xpath('./@id').get()
            item['id'] = pid
            item['big_class'] = big_class
            item['small_class'] = small_class
            item['price'] = float(book.xpath('./p[@class="price"]/span[@class="search_now_price"]/text()').get()[1:])
            item['comment'] = book.xpath('./p[@class="detail"]/text()').get()
            item['sales'] = int(book.xpath('./p[@class="search_star_line"]/a/text()').get()[:-3])
            item['stock'] = random.randint(1000, 10000)

            images_url = book.xpath('./a/@href').get()
            yield Request(url=images_url, callback=self.parse_images_and_name, meta={'info': item})

    def parse_images_and_name(self, response):
        item = response.meta['info']
        item['name'] = response.xpath('//div[@class="name_info"]/h1/@title').get()
        item['images'] = response.xpath('//ul[@id="main-img-slider"]/li/a/@data-imghref').extract()[:5]

        pid = item['id']
        reply_url = 'http://product.dangdang.com/index.php?r=comment%2Flist&productId={}&categoryPath=01.41.05.03.00.00&mainProductId={}&mediumId=0&pageIndex=1&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0&template=publish'.format(
            pid[1:], pid[1:])
        yield Request(reply_url, self.parse_reply, meta={'info': item})

    def parse_reply(self, response):
        item = response.meta['info']
        user_list = []
        res = json.loads(response.text)
        html = Selector(text=res['data']['list']['html'])
        users = html.xpath('//div[@class="comment_items clearfix"]')
        for user in users:
            user_info = {
                'content': user.xpath(
                    './div[@class="items_right"]/div[@class="describe_detail"]/span/a/text()').get(),
                'date': user.xpath('./div[@class="items_right"]/div[@class="starline clearfix"]/span/text()').get(),
                'username': user.xpath('./div[@class="items_left_pic"]/span[@class="name"]/text()').get(),
                'img': user.xpath('./div[@class="items_left_pic"]/a/img/@src').get()
            }
            user_list.append(user_info)
        item['reply'] = user_list
        return item