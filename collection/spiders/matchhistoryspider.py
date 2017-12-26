# author : YangWan
# -- coding: utf-8 --
from scrapy import Spider
from scrapy import Request
from collection.items import MatcherData
import logging

class MatchHistorySpider(Spider):

    name = 'matchhistoryspider'

    index = 0

    allowed_domains = ["http://zx.500.com"]

    start_urls = ['http://zx.500.com/zqdc/inc/shuju_saishi.php']

    '''
        爬取页面url示例:
        http://zx.500.com/zqdc/inc/shuju_saishi.php?gt=ajax&pn=1&pt=2&mc=82&bt=2007-11-1&et=2017-11-28&rq=&tm=0
        gt数据格式，pn页码翻页
        初始化参数，pt(tab分页参数), mc(赛事类型)， bt(开始日期), et(结束日期),rq(让球个数)，tm(球队)
    '''

    def __init__(self, category=None, *args, **kwargs):
        super(MatchHistorySpider, self).__init__(*args, **kwargs)
        self.category = category
        self.has_page = False #是否执行分页操作，兼容网页改变
        self.pn = kwargs['pn_params']
        self.pt = kwargs['pt_params']
        self.mc = kwargs['mc_params']
        self.bt = kwargs['bt_params']
        self.et = kwargs['et_params']
        self.rq = kwargs['rq_params']
        self.tm = kwargs['tm_params']

    def start_requests(self):
        pages = []
        crawl_url = self.get_changepage_url(self.pn)
        page = Request(crawl_url)
        pages.append(page)
        return pages

    def get_changepage_url(self, page_index):
        crawl_url = self.start_urls[0] + '?gt=ajax&' + 'pt=' + self.pt + '&mc=' + self.mc + '&bt=' + \
                    self.bt + '&et=' + self.et + '&rq=' + self.rq + '&tm=' + self.tm
        if self.has_page is True:
            crawl_url += '&pn=' + page_index
        return crawl_url

    def parse(self, response):
        logging.info("crawling url of the page: %s", response.url)
        data_table = response.xpath("//table[@class='ld_table']")
        if len(data_table) != 0:
            tbody_data_tr = data_table.xpath("tr")
            print '*********', len(tbody_data_tr)
            if len(tbody_data_tr) > 0:
                for index in range(1, len(tbody_data_tr)):
                    data_td = tbody_data_tr[index].xpath("td")
                    item = MatcherData()
                    # 获取赛事类型
                    item['eventtype'] = data_td[0].xpath("text()").extract()[0]
                    # 获取比赛时间
                    item['matchertime'] = data_td[2].xpath("text()").extract()[0]
                    # 获取主队名称
                    item['hometeam'] = data_td[3].xpath("a/text()").extract()[0]
                    # 获取让球
                    item['letball'] = data_td[4].xpath("text()").extract()
                    if (len(item['letball']) == 0):
                        item['letball'] = data_td[4].xpath("span/text()").extract()[0]
                    else:
                        item['letball'] = data_td[4].xpath("text()").extract()[0]
                    # 获取客队名称
                    item['visitingteam'] = data_td[5].xpath("a/text()").extract()[0]
                    item['score'] = data_td[6].xpath("text()").extract()[0]
                    item['collection'] = data_td[7].xpath("text()").extract()[0]
                    item['collectionsp'] = data_td[9].xpath("text()").extract()[0]
                    item['compensatewin'] = data_td[11].xpath("text()").extract()[0]
                    item['compensateflat'] = data_td[12].xpath("text()").extract()[0]
                    item['compensatenegative'] = data_td[13].xpath("text()").extract()[0]
                    # logging.info("yield data item : %s", item.__str__())
                    #返回爬取数据
                    yield item
            else:
                logging.info("数据列表为空（%d）", len(tbody_data_tr))
        else:
            logging.info("the data is empty, the crawl url is %s", response.url)
