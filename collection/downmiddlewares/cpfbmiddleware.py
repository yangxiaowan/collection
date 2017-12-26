# author : YangWan
# -*- coding: utf-8 -*-

from selenium import webdriver
from scrapy.http import HtmlResponse
import re
import logging
import time

logger = logging.getLogger(__name__)
class CpFbMiddleware(object):

    def process_request(self, request, spider):
        #检查是否是爬取历史赛果，如果是则启动中间件
        pattern = re.compile(r'^http://info.sporttery.cn/football/history/history_data.php\?mid=\d+&s_id=\d+')
        match = pattern.match(request.url)
        if match:
            driver = webdriver.PhantomJS("C:/dptools/phantomjs-2.1.1-windows/bin/phantomjs.exe")
            try:
                driver.implicitly_wait(3)
                logger.info("ready to download the page, url: %s", request.url)
                driver.get(request.url)
                # look_more = ".//td[@id='12595']/a"
                look_more = ".//a[@class='pols']"
                driver.find_element_by_xpath(look_more).click()
                true_page = driver.page_source
                driver.close()
                return HtmlResponse(request.url,
                                    body=true_page,
                                    encoding='utf-8',
                                    request=request, )
            except:
                print "get news data failed"
        else:
            return None
