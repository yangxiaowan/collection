# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from collection.utils.httpproxy import Proxies

class MyCustomDownloaderMiddleware(object):

    ip_index = 0

    ip_pool = ['http://117.78.50.121:8118', ]

    #从ip代理池获取动态ip
    # def process_request(self, request, spider):
    #     # 125.45.87.12:9999
    #     pass

    #设置动态ip
    # def process_request(self, request, spider):
    #     '''对request对象加上proxy'''
    #     proxy = 'http://125.45.87.12:9999'
    #     print("this is request ip:" + proxy)
    #     request.meta['proxy'] = proxy

    # def process_response(self, request, response, spider):
    #     # 如果返回的response状态不是200，重新生成当前request对象
    #     if response.status != 200:
    #         proxy = self.get_next_proxy()
    #         print("this is response ip:" + proxy)
    #         # 对当前reque加上代理
    #         request.meta['proxy'] = proxy
    #         return request
    #     return response

            #设置为下一个ip代理
    def get_next_proxy(self):
        #如果ip_index使用完毕
        if self.ip_index == -1:
            self.ip_pool = Proxies().getProxiesList()
        if self.ip_index == len(self.ip_pool):
            self.ip_index = 0
        self.ip_index += 1
        return self.ip_pool[self.ip_index - 1]


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
