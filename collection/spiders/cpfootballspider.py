# author : YangWan
# -*- coding: utf-8 -*-
from scrapy import Spider
from collection.items import EventType
import logging
from scrapy import Request
import scrapy

class cpfootballspider(Spider):

    name = 'cpfootballspider'

    page_index = None

    allowed_domains = 'http://info.sporttery.cn'

    history_url = 'http://info.sporttery.cn/football/history/history_data.php'

    start_urls = [
        'http://info.sporttery.cn/football/history/data_center.php',
    ]

    def parse(self, response):
        logging.info("the url of website: %s", response.url)
        #解析赛事类型
        # yield Request(url=response.url, callback=self.parse_details)
        yield scrapy.http.Request(response.url, callback=self.parse_match_event, dont_filter=True)

    def parse_match_event(self, response):
        match_menu_div = response.xpath("//div[@class='match-menu']")
        #存储赛事类型的数组 分为欧洲赛事 美洲赛事 亚洲赛事 国际赛事
        event_class_list = {}
        event_class_li = match_menu_div.xpath("ul[@id='tab']/li")
        for event_class_liitem in event_class_li:
            key_value = event_class_liitem.xpath("@num").extract()[0]
            event_class_list[key_value] = event_class_liitem.xpath("text()").extract()[0]
        content_div = response.xpath("//div[@class='match-info']")
        logging.info("赛事类别信息抓取: %s", event_class_list)
        #找到所有的赛事列表
        event_class_div = content_div.xpath("div")
        logging.info("国家类别个数: %d", len(event_class_div))
        for event_class_div_item in event_class_div:
            #获得国家名称
            event_country_name = event_class_div_item.xpath("div[@class='match-name']/div/text()").extract_first()
            event_li_list = event_class_div_item.xpath("div[@class='match-box']//li")
            list_key_value = event_class_div_item.xpath("@num").extract()[0]
            for event_li_item in event_li_list:
                event_item = EventType()
                #提取出赛事id
                event_li_item_a = event_li_item.xpath("a")[0]
                event_item['eventid'] = event_li_item_a.xpath("@href").re(r'^history_data.php\?mid\=(.*)')[0]
                print event_item['eventid']
                event_item['event'] = event_li_item_a.xpath("text()").extract()[0]
                event_item['eventyclass'] = event_class_list[list_key_value]
                event_item['eventcountry'] = event_country_name
                yield event_item
        #跳转至特定赛事解析页面，获取对症赛果和庄家赔率
        # matcher_detail_url = self.history_url + ("?mid=%s" % (event_item['eventid'].strip(), ))
        # self.page_index = None
        # yield scrapy.http.Request(matcher_detail_url, callback=self.parse_match_compsection, dont_filter=True)
