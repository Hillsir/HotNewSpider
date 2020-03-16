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
            if not self.filter_url(url):
                pass
            else:
                yield Request(url, meta={"source_url": url}, callback=self.get_details)

    def get_details(self, response):

        item = HotNewsItem()

        content = []
        for x in response.xpath('//div[@class="post_text"]/p'):
            x = x.xpath('text()').extract()
            if x:
                x = x[0].strip()
                if x:
                    content.append(x)
        item['content'] = content
        classify = response.xpath(
            '//div[@class="post_crumb"]//a[2]/text()').get()

        item['source_url'] = response.meta['source_url']
        title, classification = self.hendle_title(
            response.xpath('//title/text()').get())
        item['title'] = title
        item['classification'] = self.filter_classification(classify if classify else classification)

        if not title and not content:
            return


        yield item

    def filter_url(self, url):
        for i in ['play', 'auto','dy']:
            if i in url:
                return False
        return True

    def hendle_title(self, string: str):
        if string and '_' in string:
            string = string.split('_')
            return string[0], string[1]
        else:
            return string, '新闻'

    def filter_classification(self, classification:str):
        for i in ['网易','频道','中心']:
            if i in classification:
                classification = classification.replace(i,'')
        return classification
