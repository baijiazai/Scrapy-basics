# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('./span/small/text()').extract_first()
            }
        # 下一页
        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)
