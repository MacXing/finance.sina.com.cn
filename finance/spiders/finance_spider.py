# -*- coding: utf-8 -*-
import scrapy
from finance import items,select_url

class FinanceSpiderSpider(scrapy.Spider):
    name = 'finance_spider'
    allowed_domains = ['sina.com']
    start_urls = ['http://finance.sina.com.cn/']
    results = select_url.serch_url()
    urls = []

    def parse(self, response):

        url_list = response.xpath('//a/@href').extract()

        if url_list:
            for url in url_list:
                if 'finance.sina.com' in url:
                    if url not in self.results:
                        self.urls.append(url)
        else:
            self.log('no url ---%s' % response.url)

        print(len(self.urls))

        for url in self.urls:
            self.urls = list(set(self.urls))
            item = items.FinanceItem()
            item['url'] = url
            # self.urls.remove(url)
            yield scrapy.Request(url=item['url'], meta={'item': item}, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):

        url_list = response.xpath('//a/@href').extract()

        if url_list:
            for url in url_list:
                if 'finance.sina.com' in url:
                    if url not in self.results:
                        self.urls.append(url)

            else:
                self.log('no url ---%s' % response.url)

        print(len(self.urls))
        item = response.meta['item']
        if len(response.xpath('//h1[@class="main-title"]/text()').extract()) > 0:
            item['title'] = response.xpath('//h1[@class="main-title"]/text()').extract()[0]
            if len(response.xpath('//div[@class="channel-path"]/a/text()')) > 0:
                item['tag'] = response.xpath('//div[@class="channel-path"]/a/text()').extract()[0]
            else:
                item['tag'] = ''
            item['time'] = response.xpath('//div/span[@class="date"]/text()').extract()[0]
            if len(response.xpath('//div/span[@class="source ent-source"]/text()').extract()) > 0:
                item['resource'] = response.xpath('//div/span[@class="source ent-source"]/text()').extract()[0]
            else:
                item['resource'] = ''
            content = response.xpath('//div[@class="article"]/p/text()').extract()
            item['content'] = ''.join(content).replace('\u3000', '').replace('\xa0', '')

            self.log("success download url :  %s" % response.url)

            return item
        else:
            self.log('error page !')
