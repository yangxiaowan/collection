# author : YangWan
# -- coding: utf-8 --
from scrapy import Spider
from scrapy.http import Request
from collection.items import XiciFreeIp
import time
import logging

'''
xici代理爬取工具 有严格防爬取机制

'''

logger = logging.getLogger(__name__)
class XiciDailiSpider(Spider):

    name = 'xicidailispider'

    allowed_domains = ['http://www.xicidaili.com/']

    #默认爬取代理为http代理
    start_parse_url = 'http://www.xicidaili.com/wt'

    category = None

    #默认爬取页数为10页，改参数在启动爬虫的时候重新设置，key为scraindex
    default_scraindex = 1

    #代理总页数
    total_page_num = 1

    def __init__(self, category=None, *args, **kwargs):
        super(XiciDailiSpider, self).__init__(*args, **kwargs)
        if category is not None:
            self.category = category
        if 'scraindex' in kwargs.keys():
            self.default_scraindex = int(kwargs['scraindex'])

    def start_requests(self):
        if self.category is not None:
            self.start_parse_url = self.allowed_domains[0] + self.category
        yield Request(self.start_parse_url, callback=self.parse, dont_filter=True)

    #获得可爬取代理页面总条数，具体爬取页面数量有参数default_scraindex决定
    def get_total_page(self, pagination_div):
        if len(pagination_div) > 0:
            pagination_div_alist = pagination_div[0].xpath("a")
            alist_len = len(pagination_div_alist)
            if alist_len > 2:
                self.total_page_num = int(pagination_div_alist[alist_len-2].xpath("text()").extract_first().strip())

    #翻页解析
    def parse(self, response):
        logging.info("初始爬取页面: %s", self.start_parse_url)
        self.get_total_page(response.xpath("//div[@class='pagination']"))
        logging.info("可爬页面总条数: %d", self.total_page_num)
        for page_index in range(1, self.default_scraindex + 1, 1):
            next_parse_url = self.start_parse_url + "/" + str(page_index)
            yield Request(next_parse_url, callback=self.parse_free_ip, dont_filter=True)

    #免费ip入库
    def parse_free_ip(self, response):
        ip_list_table = response.xpath("//table[@id='ip_list']")
        ip_content_tr = ip_list_table.xpath("tr")
        logging.info("爬取页面地址: %s,  页面数据条数: %d", response.url, len(ip_content_tr))
        for ip_content_tr_item in ip_content_tr:
            ip_content_td_list = ip_content_tr_item.xpath("td")
            if len(ip_content_td_list) == 10:
                xicifreeip = XiciFreeIp()
                xicifreeip['country'] = ip_content_td_list[0].xpath("img/@alt").extract_first()
                xicifreeip['ipstr'] = ip_content_td_list[1].xpath("text()").extract_first()
                xicifreeip['port'] = ip_content_td_list[2].xpath("text()").extract_first()
                xicifreeip['serverlocal'] = ip_content_td_list[3].xpath("a/text()").extract_first()
                xicifreeip['ishide'] = ip_content_td_list[4].xpath("text()").extract_first()
                xicifreeip['httptype'] = ip_content_td_list[5].xpath("text()").extract_first()
                speed_str = ip_content_td_list[6].xpath("div[@class='bar']/@title").re(r'(\d*\.\d*)')[0]
                xicifreeip['speed'] = float(speed_str)
                connecttime_str = ip_content_td_list[7].xpath("div[@class='bar']/@title").re(r'(\d*\.\d*)')[0]
                xicifreeip['connecttime'] = float(connecttime_str)
                xicifreeip['alivetime'] = ip_content_td_list[8].xpath("text()").extract_first()
                xicifreeip['verifytime'] = ip_content_td_list[9].xpath("text()").extract_first() + ":00"
                xicifreeip['lastupdate'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                print xicifreeip
                yield xicifreeip

