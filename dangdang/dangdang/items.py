# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookInfoItem(scrapy.Item):
    big_class = scrapy.Field()
    small_class = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    sales = scrapy.Field()
    comment = scrapy.Field()
    reply = scrapy.Field()


class DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
