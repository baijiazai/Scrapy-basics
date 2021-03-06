# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QianmuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ranking = scrapy.Field()
    c_name = scrapy.Field()
    e_name = scrapy.Field()
    city = scrapy.Field()
    tuition = scrapy.Field()
    number = scrapy.Field()
    sat_avg = scrapy.Field()
    atc_avg = scrapy.Field()
