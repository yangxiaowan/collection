# author : YangWan
# -- coding: utf-8 --
import scrapy
from collection.items import LottKjItem

class LottScrapySpider(scrapy.Spider):
    name = "lottscra"
    allowed_domains = ["www.500.com"]
    start_urls = [
        "http://www.500.com/"
    ]

    def parse(self, response):
        title = response.xpath('/html/head/title')
        print title
        products = response.xpath("//ul[@class='tabs-nav ont_tab']/li/text()").extract()
        print products, str(len(products))
        print products[0].encode('utf-8'), products[1].encode('utf-8'), products[2].encode('utf-8')
        # print products[0].encode('utf-8'), products[1].encode('utf-8'), products[2].encode('utf-8')
        kjdiv = response.xpath("//div[@class='tabs-cnt scroll_box']")
        items = []
        i = 0

        # 爬取500彩票网站-竞技彩票开奖号码
        for kjdiv_item in kjdiv:
            kjsite = kjdiv_item.xpath("//dl[@class='kj_sort']")
            print kjsite, str(len(kjsite))
            for kesite_item in kjsite:
                item = LottKjItem()
                item['product'] = products[i].encode('utf-8')
                print item['product'] + "彩票开奖信息如下: "
                item['lotterytype'] = kesite_item.xpath('dt/a/text()').extract()[0].encode('utf-8')
                print item['lotterytype']
                item['product'] = products[i]
                item['lottno'] = kesite_item.xpath("dt/span[@class='eng']/text()").extract()[0]
                print item['lottno']
                item['kjnum'] = kesite_item.xpath("dd[@class='kj_num eng']/text()").extract()[0]
                print item['kjnum']
                items.append(item)
                yield item
            i = i + 1
            print i
