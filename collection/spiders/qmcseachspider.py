# author : YangWan
# -*- coding: utf-8 -*-

from scrapy import Spider
from scrapy.http import Request
from collection.items import RelevantSearchItem
from collection.items import QmcSeachItem
import re
import logging

logger = logging.getLogger(__name__)
class QmcSeachSipder(Spider):

    name = 'qmcbaiduspider'

    page_index = None

    start_urls_dit = {'baidu': 'https://www.baidu.com/s?wd=',
                      'sogou': 'https://www.sogou.com/web?query=',
                      '360': 'https://www.so.com/s?q=',
                      }

    #默认爬取页数为1
    pagenum = 1

    #相关搜索
    relevant_search = False

    #开始网站排名
    rank_index = 0

    #推荐搜索
    recommend_search = False

    #推荐搜索存储item
    relevant_item = None

    '''
    参数定义:
    category:搜索引擎种类
    args&kwargs:搜索参数 
    keyword(搜索关键) pagenum(搜索页面数量)
    '''
    def __init__(self, category='baidu', *args, **kwargs):
        self.category = category
        self.start_page_url = self.start_urls_dit[category]
        if 'keyword' in kwargs.keys() and kwargs['keyword'] is not None:
            self.keyword = kwargs['keyword']
        else:
            logging.error('params error!')
            raise Exception("the params keyword is none")
        if 'pagenum' in kwargs.keys() and kwargs['pagenum'] is not None:
            self.pagenum = int(kwargs['pagenum'])

    '''
    请求参数加入url
    '''
    def start_requests(self):
        for index in range(1, self.pagenum + 1):
            start_url = self.start_page_url + self.keyword
            if self.category == 'baidu':
                page_start_index = (index - 1) * 10
                start_url = start_url + '&pn=' + str(page_start_index)
                yield Request(start_url, callback=self.parse_baidu_page, dont_filter=True)
            elif self.category == 'sogou':
                page_start_index = index
                start_url = start_url + '&page=' + str(page_start_index)
                yield Request(start_url, callback=self.parse_sogou_page, dont_filter=True)
            elif self.category == '360':
                page_start_index = index
                start_url = start_url + '&pn=' + str(page_start_index)
                yield Request(start_url, callback=self.parse_360_page, dont_filter=True)

    '''
    百度搜索引擎爬取搜索结果
    '''
    def parse_baidu_page(self, response):
        logging.info("crawled from the url : " + response.url)
        content_left_div = response.xpath("//div[@id='content_left']")
        content_div_list = content_left_div.xpath("div[contains(@class, 'c-container')]")
        if len(content_div_list) > 0:
            #获得推荐字段列表
            recommend_list = response.xpath(
                "//div[@class='hint_toprq_tips f13 se_common_hint']/span[@class='hint_toprq_tips_items']//div")
            if self.recommend_search is False and len(recommend_list) > 0:
                self.relevant_item = RelevantSearchItem()
                self.relevant_item['keyword'] = self.keyword
            #循环每个div，获得对应爬取网站
            for search_index in range(0, len(content_div_list)):
                baidu_item = QmcSeachItem()
                #获得每条搜索记录的页面标题
                self.rank_index += 1
                baidu_item['rankindex'] = self.rank_index
                content_div_item = content_div_list[search_index]
                content_div_css = content_div_item.xpath("@class").extract_first()
                if str(content_div_css) == 'result c-container ' or str(content_div_css)\
                        == 'result-op c-container xpath-log':
                    title_h3 = content_div_item.xpath(".//h3[contains(@class, 't')]")
                    #获得标题
                    title = title_h3.xpath("string(a)").extract_first()
                    baidu_item['seachtitle'] = title
                    #获得页面地址
                    pageurl_desc = title_h3.xpath("a/@href").extract_first()
                    baidu_item['pageurl'] = pageurl_desc
                    baidu_item['websiteurl'] = \
                        content_div_item.xpath("//div[@class='f13']/a/text()").extract_first().strip()
                    if str(content_div_css) == 'result c-container ':
                        #获得基本描述信息
                        cabstract_desc = \
                            content_div_item.xpath("string(.//div[contains(@class, 'c-abstract')])").extract_first()
                        baidu_item['seachdesc'] = cabstract_desc
                    elif str(content_div_css) == 'result-op c-container xpath-log':
                        cabstract_desc = content_div_item.xpath("string(.//div[@class='c-span18 c-span-last']/p)")\
                            .extract_first().strip()
                        baidu_item['seachdesc'] = cabstract_desc
                    print self.rank_index, title, pageurl_desc, cabstract_desc, baidu_item['websiteurl']
                else:
                    print 'exception', self.rank_index, content_div_list[search_index], search_index
    '''
    搜狗搜索引擎爬取结果
    '''
    def parse_sogou_page(self, response):
        logging.info("crawled from the url : " + response.url)
        result_div = response.xpath("//div[@class='results']")
        #获得页面推荐项目
        recommend_box = response.xpath("//div[@class='top-hintBox']")
        #如果之前没有解析相关推荐，且有相关推荐进入解析程序
        if self.recommend_search is False and len(recommend_box) > 0:
            recommend_text_list = recommend_box[0].xpath("dl/dd/a/text()").extract()
            if self.relevant_item is None:
                self.relevant_item = RelevantSearchItem()
            recommend_str = ''
            for temp_str in recommend_text_list:
                recommend_str += temp_str
                recommend_str += ','
            self.relevant_item['keyword'] = self.keyword
            self.relevant_item['recommendword'] = recommend_str
            logging.info("Sogou recommends a search term: " + recommend_str)
        content_div = result_div.xpath("div")
        logging.info("the number of the page term: %d", len(content_div))
        for content_div_item in content_div:
            qmcseachitem = None
            title_h3_a = content_div_item.xpath("h3/a")
            if len(title_h3_a) > 0:
                self.rank_index += 1
                if qmcseachitem is None:
                    qmcseachitem = QmcSeachItem()
                qmcseachitem['seachtitle'] = title_h3_a.xpath("string()").extract_first()
                qmcseachitem['pageurl'] = title_h3_a.xpath("@href").extract_first()
                str_info_p = content_div_item.xpath(".//p[@class='str_info']")
                if len(str_info_p) == 0:
                    str_info_p = content_div_item.xpath("div[@class='ft']")
                search_desc = str_info_p.xpath("string()").extract_first()
                if len(str_info_p) == 0:
                    second_div = content_div_item.xpath("div")
                    if len(second_div) > 0:
                        search_desc = second_div[0].xpath("string()").extract_first()
                        search_desc = re.sub('[\r\n\t\b ]', '', search_desc)
                qmcseachitem['seachdesc'] = search_desc
                fb_div_cite = content_div_item.xpath(".//div[@class='fb']/cite")
                if len(fb_div_cite) > 0:
                    qmcseachitem['websiteurl'] = fb_div_cite.xpath("text()").extract_first()
                qmcseachitem['rankindex'] = self.rank_index
                print qmcseachitem['rankindex'], qmcseachitem['seachtitle'], \
                    qmcseachitem['websiteurl'], qmcseachitem['seachdesc'], qmcseachitem['pageurl']

    '''
    360搜索引擎爬取结果
    '''
    def parse_360_page(self, response):
        logging.info("crawled from the url : " + response.url)
        warper_div_list = response.xpath("//div[@id='warper']")
        if len(warper_div_list) > 0:
            warper_div = warper_div_list[0]
            recommend_dl = warper_div.xpath(".//div[@id='so_top']")
            #如果有相关推荐词条，进入相关推荐词条解析
            if len(recommend_dl) > 0:
                recommend_dl_ddlist = recommend_dl.xpath("dl/dd/a/text()").extract()
                recommend_str = ''
                for temp_str in recommend_dl_ddlist:
                    recommend_str += temp_str
                    recommend_str += ','
                logging.info("360 recommends a search term: " + recommend_str)
            result_ul = warper_div.xpath(".//ul[@class='result']")
            #进入词条搜索的相关网站解析
            if len(result_ul) > 0:
                result_ul_list = result_ul.xpath("li")
                for result_ul_item in result_ul_list:
                    qmcseachitem = None
                    title_h3_a = result_ul_item.xpath(".//h3[contains(@class, 'title')]/a")
                    if len(title_h3_a) > 0:
                        if qmcseachitem is None:
                            qmcseachitem = QmcSeachItem()
                        title = title_h3_a.xpath("string()").extract_first()
                        qmcseachitem['seachtitle'] = title
