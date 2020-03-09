# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import HotNewsItem


class A163newSpider(scrapy.Spider):
    name = '163new'
    allowed_domains = ['163.com']
    start_urls = ['http://news.163.com/rank/']

    def parse(self, response):
        for i in response.xpath('//div[@class="tabBox"]//div[@class="tabContents"][2]//td//a'):

            url = i.xpath('@href').get()
            title = i.xpath('text()').get()
            yield Request(url, meta={"source_url": url, "title": title}, callback=self.get_details)

    def get_details(self, response):

        item = HotNewsItem()
        item['content'] = [x.get()
                           for x in response.xpath('//div[@class="post_text"]//p//text()')]
        classify = response.xpath(
            '//div[@class="post_crumb"]//a[2]/text()').get()

        item['classification'] = classify if classify else "新闻"
        item['source_url'] = response.meta['source_url']
        item['title'] = response.meta['title']
        yield item
