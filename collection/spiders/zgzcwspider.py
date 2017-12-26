# author : YangWan
# -- coding: utf-8 --

import scrapy
from collection.items import ZgzcwItem
from datetime import date, datetime

class ZgzcwSpider(scrapy.Spider):

    name = "zgzcwspider"

    allowed_domains = "www.zgzcw.com"

    start_urls = [
        "http://www.zgzcw.com"
    ]

    #爬取足彩网站开奖信息
    def parse(self, response):
        items = []
        kj_div = response.xpath("//div[@class='m-1-cons zxkj']")
        print kj_div
        header_div = kj_div.xpath("div[@class='m-1-cons-head']")
        classifications = []
        class_li = header_div.xpath("ul[@id='tabs_kj']/li")
        #获得开奖彩票分类
        for li_item in class_li:
            class_name = li_item.xpath("text()").extract()[0]
            classifications.append(class_name)
            print "add the lottery classification: " + class_name
        #获得具体开奖信息
        now_day = date.today()
        now_day_year = str(now_day.year)
        klhis_div = kj_div.xpath("//div[@class='klHis']")
        class_index = 0
        print klhis_div
        for klhis_item in klhis_div:
            kj_ul = klhis_item.xpath("ul")
            print len(kj_ul)
            for kj_ulitem in kj_ul:
                item = ZgzcwItem()
                item['classification'] = classifications[class_index].encode('utf-8')
                item['lotterytype'] = kj_ulitem.xpath("li/div[@class='zxkjc1']/span/text()").extract()[0]
                item['period'] = kj_ulitem.xpath("li/div[@class='zxkjc1']/b/text()").extract()[0]
                item['kjtime'] = now_day_year + "-" +kj_ulitem.xpath("li/div[@class='zxkjc1']/text()").extract()[0]
                # print datetime.strptime(item['kjtime'], "%Y-%m-%d %H:%M")
                print item['classification'], item['lotterytype'], item['period'], item['kjtime']
                kj_result_div = kj_ulitem.xpath("li/div[@class='zxkjc2']")
                print kj_result_div
                kj_result_li = kj_result_div.xpath("i")
                if(len(kj_result_li) == 0):
                    #开奖接口无样式，直接获取div中的文字存入item
                    item['kjresult'] = kj_result_div.xpath("text()").extract()[0]
                else:
                    #根据开奖接口数字样式拼接开奖信息数字
                    kjresult = ''
                    for kj_li in kj_result_li:
                        kjresult += kj_li.xpath("text()").extract()[0]
                        kjresult += ' '
                    item['kjresult'] = kjresult
                    print "***************merge kjresult :", kjresult
                items.append(item)
                yield item
            class_index += 1
        print items.__str__(), "get the number of items: ", len(items)