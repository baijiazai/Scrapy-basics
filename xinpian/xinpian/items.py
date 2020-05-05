# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ComposerItem(scrapy.Item):
    table_name = 'composer'
    banner = scrapy.Field()
    nickname = scrapy.Field()
    description = scrapy.Field()
    like_counts = scrapy.Field()
    fans_counts = scrapy.Field()
    concern = scrapy.Field()
    location = scrapy.Field()
    profession = scrapy.Field()


class XinpianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
