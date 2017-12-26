# author : YangWan
# -- coding: utf-8 --
from scrapy import Spider
from scrapy import Request
from collection.items import MatcherData
import logging


logger = logging.getLogger(__name__)
class CaikeLottSpider(Spider):

    name = 'caikespider'

    allowed_domains = ['zx.500.com']

    start_urls = ['http://zx.500.com/zqdc/shuju.php']

    '''
        爬取页面url示例:
        http://zx.500.com/zqdc/shuju.php?pt=1&mc=522&bt=2007-11-1&et=2017-11-28&rq=&tm=0
        初始化参数，pt(分页参数), mc(赛事类型)， bt(开始日期), et(结束日期),rq(让球个数)，tm(球队)
    '''

    def __init__(self, category=None, *args, **kwargs):
        super(CaikeLottSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.pt = kwargs['pt_params']
        self.mc = kwargs['mc_params']
        self.bt = kwargs['bt_params']
        self.et = kwargs['et_params']
        self.rq = kwargs['rq_params']
        self.tm = kwargs['tm_params']

    '''
        根据参数构造url，使用get方式请求页面
    '''
    def start_requests(self):
        pages = []
        crawl_url = self.start_urls[0] + '?pt=' + self.pt + '&mc=' + self.mc + '&bt=' + self.bt + \
                    '&et=' + self.et + '&rq=' + self.rq + '&tm=' + self.tm
        page = Request(crawl_url)
        pages.append(page)
        return pages


    def change_page(self, page_index):
        crawl_url = self.start_urls[0] + '?pt=' + self.pt + '&mc=' + self.mc + '&bt=' + self.bt + \
                    '&et=' + self.et + '&rq=' + self.rq + '&tm=' + self.tm
    '''
        根据参数爬取历史数据
    '''
    def parse(self, response):
        logging.info("crawling url of the page: %s", response.url)
        matcher_data_div = response.xpath("//div[@id='saishi_data']")
        logging.info("爬取数据div定位: %s", matcher_data_div)
        tbody_data_tr = matcher_data_div.xpath("table/tr")
        url_temp = response.url
        if(len(tbody_data_tr) > 0):
            for index in range(1, len(tbody_data_tr)):
                data_td = tbody_data_tr[index].xpath("td")
                item = MatcherData()
                # 获取赛事类型
                item['eventtype'] = data_td[1].xpath("a/text()").extract()[0]
                # 获取比赛时间
                item['matchertime'] = data_td[2].xpath("text()").extract()[0]
                # 获取主队名称
                item['hometeam'] = data_td[3].xpath("a/text()").extract()[0]
                # 获取让球
                item['letball'] = data_td[4].xpath("text()").extract()
                if(len(item['letball']) == 0):
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
                # yield item
        else:
            logging.info("数据列表为空（%d）", len(tbody_data_tr))
        # id_multpage_div = response.xpath("//div[@id='multpage']")
        # print id_multpage_div
        # a_temp = id_multpage_div.xpath("a")
        # print a_temp
        # div_temp = id_bottom_div.xpath("div")
        # print div_temp
        # index_a = div_temp.xpath("a[@id='link188']")
        # print index_a
        # for index_a_item in index_a:
        #     print index_a_item.xpath("text()").extract()[0]
