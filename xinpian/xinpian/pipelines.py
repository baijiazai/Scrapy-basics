# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class XinpianPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='xinpian',
            user='root',
            password='',
            charset='utf8'
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        keys, values = zip(*item.items())
        sql = 'insert into {} ({}) values ({})'.format(
            item.table_name,
            ','.join(keys),
            ','.join(['%s'] * len(values))
        )
        self.cur.execute(sql, values)
        self.conn.commit()
        print(self.cur._last_executed)
        return item
