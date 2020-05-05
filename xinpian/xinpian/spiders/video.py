# -*- coding: utf-8 -*-
import json
import re
import string
import random

import scrapy
from scrapy import Request

cookies = {
    'Authorization': 'D6FCBCCA2638248E62638245E5263829C1126382B1EDFA613BB7'
}


def gen_session_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=26))


class VideoSpider(scrapy.Spider):
    name = 'video'
    allowed_domains = ['www.xinpianchang.com', 'openapi-vtom.vmovier.com', 'app.xinpianchang.com']
    start_urls = ['https://www.xinpianchang.com/channel/index/sort-like?from=navigator']
    page_count = 0

    def parse(self, response):
        videos = response.xpath('//ul[@class="video-list"]/li/@data-articleid').extract()
        for video in videos:
            url = 'https://www.xinpianchang.com/a%s?from=ArticleList' % video
            request = response.follow(url, self.parse_info)
            request.meta['video_id'] = video
            yield request

        self.page_count += 1
        if self.page_count >= 50:
            self.page_count = 0
            cookies.update(PHPSESSID=gen_session_id())

        next_page = response.xpath('//div[@class="page"]/a[@title="下一页"]/@href').get()
        if next_page:
            next_page_url = 'https://www.xinpianchang.com' + next_page
            yield response.follow(next_page_url, self.parse, cookies=cookies)

    # 视频详情
    def parse_info(self, response):
        info = {}
        cate_list = response.xpath('//span[contains(@class, "cate")]//text()').extract()
        info['cate'] = ''.join([cate.strip() for cate in cate_list])
        info['update_time'] = response.xpath('//span[contains(@class, "update-time")]/i/text()').get()
        info['play_counts'] = response.xpath('//i[contains(@class, "play-counts")]/@data-curplaycounts').get()
        info['like_counts'] = response.xpath('//span[contains(@class, "like-counts")]/@data-counts').get()
        desc_list = response.xpath('//p[contains(@class, "desc")]/text()').extract()
        info['description'] = ' '.join([desc.strip() for desc in desc_list])

        vid = re.findall('vid: "(.*?)"', response.text)[0]
        get_url = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource&usage=xpc_web' % vid
        request = Request(get_url, self.parse_src)
        request.meta['info'] = info
        yield request

        pid = response.meta['video_id']
        user_info_url = 'https://app.xinpianchang.com/comments?resource_id=%s&type=article&page=1&per_page=24' % pid
        request = Request(user_info_url, self.parse_comment)
        request.meta['info'] = info
        yield request

    # 视频源接口
    def parse_src(self, response):
        info = response.meta['info']
        res = json.loads(response.text)
        info['title'] = res['data']['video']['title']
        info['url'] = res['data']['resource']['default']['url']
        info['preview'] = res['data']['video']['cover']
        yield info

    # 评论接口
    def parse_comment(self, response):
        info = response.meta['info']
        res = json.loads(response.text)
        comment_list = res['data']['list']
        for comment in comment_list:
            info['user_info'] = {
                'add_time': comment['addtime'],
                'content': comment['content'],
                'user_id': comment['userid'],
                'username': comment['userInfo']['username']
            }

        next_page_url = res['data']['next_page_url']
        if next_page_url is not None:
            request = Request('https://app.xinpianchang.com' + next_page_url, self.parse_comment)
            request.meta['info'] = info
            yield request
