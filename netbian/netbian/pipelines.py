# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class NetbianPipeline(object):
    def process_item(self, item, spider):
        return item


class FourImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url, image_name in zip(item['image_urls'], item['names']):
            yield scrapy.Request(url=image_url, meta={'name': image_name})

    def file_path(self, request, response=None, info=None):
        return 'full/%s.jpg' % (request.meta['name'])
