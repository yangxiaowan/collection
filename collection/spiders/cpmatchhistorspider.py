# author : YangWan
# -*- coding: utf-8 -*-
from scrapy import Spider
import logging
import json
from scrapy import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from collection.items import CpMatchInfo

logger = logging.getLogger(__name__)
class CpMatchHistorySpider(Spider):

    name = 'cpmatchhistoryspider'

    page_index = None

    start_urls = [
        'http://info.sporttery.cn/football/history/history_data.php',
    ]

    #兼容后续爬取 参数化
    '''
    初始化参数: 赛事编号 : eventid  赛季编号: matchid
    如果matchid == None，启动页面解析赛事编号
    '''
    def __init__(self, category=None, *args, **kwargs):
        super(CpMatchHistorySpider, self).__init__(*args, **kwargs)
        self.category = category
        self.has_matchid = False
        self.eventid = kwargs['eventid']
        self.matchid = kwargs['matchid']
        self.matchid_list = []
        logging.info("params init: %s    %s", self.eventid, self.matchid)
        print "params init: ", self.eventid, self.matchid
        self.leaguename_season_dit = {}
        self.leaguenum_fz_dit = {}
        self.leaguenum_lc_dit = {}


    '''
    根据赛事编号，以及赛季编号选择起始解析页面
    '''
    def start_requests(self):
        if len(self.eventid) == 0 or (self.eventid is None):
            logger.info("CpMatchHistorySpider|ParamsException, 赛事编号不符合格式!")
            raise Exception("参数错误!")
        start_parse_url = self.start_urls[0] + "?mid=%s" % (self.eventid, )
        if len(self.matchid) > 0:
            self.has_matchid = True
        yield Request(start_parse_url, callback=self.parse, dont_filter=True)

        '''
        当参数matchid为Node的时候，解析页面获得特定赛事下的所有赛季编号
        '''
    def get_page_matchid(self, response):
        matchid_list = []
        history_div = response.xpath("//div[@class='history']")
        history_data_li = history_div.xpath("ul/li")
        for history_data_li_item in history_data_li:
            matchid = history_data_li_item.xpath("@id").extract_first().strip()
            matchid_list.append(matchid)
        return matchid_list

    '''
    爬取对象为histroy-div 获得历史联赛对应的赛事id，返回数据格式为字典
    '''
    def get_page_dit(self, response):
        matchid_dit = {}
        history_div = response.xpath("//div[@class='history']")
        history_data_li = history_div.xpath("ul/li")
        for history_data_li_item in history_data_li:
            matchid = history_data_li_item.xpath("@id").extract_first().strip()
            match_name = history_data_li_item.xpath("a/text()").extract_first()
            matchid_dit[matchid] = match_name
        return matchid_dit

    #获取赛事的赛季编号
    def parse(self, response):
        matchid_dit = self.get_page_dit(response)
        print '&&&&&&&&&&&&&&&', response.url, matchid_dit
        if self.has_matchid is False:
            self.matchid_list = matchid_dit.keys()
        else:
            self.matchid_list = self.matchid.split(",")
        #将对应的历史数据的s_id对应的赛事名称利用meta带入下一级
        for every_matchid in self.matchid_list:
            every_matchid_url = response.url + "&s_id=%s" % (every_matchid, )
            print every_matchid_url
            yield Request(every_matchid_url, callback=self.parse_every_match,
                          meta={"eventid": every_matchid, "eventname": matchid_dit[every_matchid]},
                          dont_filter=True)
        #这边赛事eventid的数量长度必须大于1，否则在start_request方法中抛出异常


    '''
    默认赛季类型 ：常规赛
    '''
    def parse_leaguename_seasons(self, response):
        #存储联赛等级的字典
        leaguename_season_dit = {}
        leaguename_season_table = response.xpath("//table[@class='league_name seasons']")
        leaguename_season_body = leaguename_season_table.xpath("tbody")
        season_grand_td = leaguename_season_body.xpath("tr//td")
        print '************', len(season_grand_td)
        dit_index = 0
        if len(season_grand_td) > 0:
            for season_grand_td_item in season_grand_td:
                temp_dic = dict()
                temp_dic["id"] = season_grand_td_item.xpath("@id").extract_first().strip()
                temp_dic['name'] = season_grand_td_item.xpath("a/text()").extract_first().strip()
                if len(season_grand_td) > 1:
                    temp_dic["cid"] = season_grand_td_item.xpath("@cid").extract_first().strip()
                    temp_dic["groups"] = season_grand_td_item.xpath("@groups").extract_first().strip()
                    temp_dic["round_type"] = season_grand_td_item.xpath("@round_type").extract_first().strip()
                    temp_dic["sid"] = season_grand_td_item.xpath("@sid").extract_first().strip()
                leaguename_season_dit[dit_index] = temp_dic
                dit_index += 1
        logging.info("解析季赛类别：%s", repr(leaguename_season_dit))
        return leaguename_season_dit

    '''
    解析div @leaguenum模块，主分页索引解析
    '''
    def parse_leaguenum_fz(self, response):
        leaguenum_fz_dit = {}
        fz_div = response.xpath("//div[@class=' fz']")
        league_num_div = fz_div.xpath("div[@class='league_num']")
        league_num_body = league_num_div.xpath("table/tbody")
        league_num_fz_td = league_num_body.xpath("tr//td")
        if len(league_num_fz_td) > 0:
           for league_num_fz_td_item in league_num_fz_td:
               fz_id = league_num_fz_td_item.xpath("@id").extract_first()
               fz_name = league_num_fz_td_item.xpath("a/text()").extract_first()
               leaguenum_fz_dit[fz_id] = fz_name
        return leaguenum_fz_dit

    def parse_leaguenum_lc(self, response):
        leaguenum_lc_dit = {}
        fz_div = response.xpath("//div[@class='lc']")
        league_num_div = fz_div.xpath("div[@class='league_num']")
        league_num_body = league_num_div.xpath("table/tbody")
        league_num_lc_td = league_num_body.xpath("tr//td")
        if len(league_num_lc_td) > 0:
           for league_num_lc_td_item in league_num_lc_td:
               lc_id = league_num_lc_td_item.xpath("@id").extract_first()
               lc_name = league_num_lc_td_item.xpath("a/text()").extract_first()
               leaguenum_lc_dit[lc_id] = lc_name
        return leaguenum_lc_dit

    def parse_match_detail(self, ls_dit, lf_dit, lc_dit, meta):
        match_action_url = 'http://info.sporttery.cn/football/history/action.php'
        print match_action_url
        if len(ls_dit) == 1 and len(lf_dit) == 0:
            league_name = ls_dit[0]['name']
            paramsdit = {}
            paramsdit['action'] = 'lc'
            paramsdit['competition_id'] = self.eventid
            paramsdit['c_id'] = self.eventid
            paramsdit['s_id'] = meta['eventid']
            paramsdit['r_id'] = ls_dit[0]['id']
            paramsdit['g_id'] = '0'
            paramsdit['table_type'] = 'whole'
            paramsdit['order_type'] = 'all'
            paramsdit['groups'] = '0'
            paramsdit['round_type'] = 'table'
            paramsdit['type1'] = 'three_-1_e'
            paramsdit['type2'] = 'asia_229_e'
            for dit_key in lc_dit.keys():
                paramsdit['week'] = lc_dit[dit_key]
                yield FormRequest(match_action_url, formdata=paramsdit, callback=self.parse_match_content)

    '''
    解析策略:  赛事类别 例如: 常规赛，半决赛决赛等 解析div @class = league_name seasons
               季赛类别 例如: 春季赛 夏季赛 解析div @class = fz, fz作为参数变量POST请求
               索引类别 例如: 分页页码，A B C D组别分类 解析div @class = lc, lc为参数变量
               赛事信息 例如: 球队对阵和赛果信息 解析div @class = match_info 创建Item，存储爬取结果
               积分榜排名 解析div @class = integral 
               积分榜解析策略: 分为全部比赛和近期比赛，场地区分为全部场地，主场，客场，作为POST参数传递
               赛事介绍 解析div @class = introduce
    '''
    def parse_every_match(self, response):
        logging.info("赛事爬取starting!!!联赛爬取地址: %s", response.url)
        #采用POST请求获得页面数据，放弃了使用middleware中间件模拟点击页面
        self.leaguename_season_dit = self.parse_leaguename_seasons(response)
        self.leaguenum_fz_dit = self.parse_leaguenum_fz(response)
        self.leaguenum_lc_dit = self.parse_leaguenum_lc(response)
        print "leaguename_season_dit: ", self.leaguename_season_dit
        print "leaguenum_fz_dit: ", self.leaguenum_fz_dit
        print "leaguenum_lc_dit: ", self.leaguenum_lc_dit
        # meta = {"eventid": every_matchid, "eventname": matchid_dit[every_matchid]}
        #上面已经解析到页面参数了，开始真正的赛事解析入库！！！
        response.meta['leaguename_season_dit'] = self.leaguename_season_dit
        match_action_url = 'http://info.sporttery.cn/football/history/action.php'
        if len(self.leaguename_season_dit) == 1 and len(self.leaguenum_fz_dit) == 0:
            if len(self.leaguenum_lc_dit) == 0:
                tr_list = response.xpath("//table[@class='league_data']/tbody//tr")
                for tr_index in range(1, len(tr_list)):
                    cpmatch_item = self.parse_match_tr(tr_list[tr_index], response)
                    yield cpmatch_item
            else:
                paramsdit = {}
                paramsdit['action'] = 'lc'
                paramsdit['competition_id'] = self.eventid
                paramsdit['c_id'] = self.eventid
                paramsdit['s_id'] = response.meta['eventid']
                paramsdit['g_id'] = '0'
                paramsdit['table_type'] = 'whole'
                paramsdit['order_type'] = 'all'
                paramsdit['groups'] = '0'
                paramsdit['round_type'] = 'table'
                paramsdit['type1'] = 'three_-1_e'
                paramsdit['type2'] = 'asia_229_e'
                paramsdit['r_id'] = self.leaguename_season_dit[0]['id']
                # paramsdit['r_id'] = '12538'
                for dit_key in self.leaguenum_lc_dit.keys():
                    paramsdit['week'] = self.leaguenum_lc_dit[dit_key]
                    yield FormRequest(match_action_url, meta=response.meta, formdata=paramsdit, callback=self.parse_match_content)
                    print 'Post请求参数: ', paramsdit
        if len(self.leaguename_season_dit) > 1:
            for dit_key in self.leaguename_season_dit.keys():
                paramsdit = {}
                paramsdit['action'] = 'round'
                paramsdit['competition_id'] = self.eventid
                paramsdit['c_id'] = self.eventid
                paramsdit['s_id'] = response.meta['eventid']
                paramsdit['r_id'] = self.leaguename_season_dit[dit_key]['id']
                paramsdit['g_id'] = '0'
                paramsdit['table_type'] = 'whole'
                paramsdit['order_type'] = 'all'
                paramsdit['groups'] = self.leaguename_season_dit[dit_key]['groups']
                paramsdit['type1'] = 'three_-1_e'
                paramsdit['type2'] = 'asia_229_e'
                paramsdit['round_type'] = self.leaguename_season_dit[dit_key]['round_type']
                response.meta['index'] = dit_key
                yield FormRequest(match_action_url, meta=response.meta, formdata=paramsdit,
                                  callback=self.parse_match_content_next)
                print 'Post请求参数: ', paramsdit


    def parse_match_weeks(self, result_str):
        league_num_div = Selector(text=result_str).xpath("//div[@class='league_num']")
        print league_num_div
        league_num_td = league_num_div.xpath("//td")
        print len(league_num_td), '-------------------------', result_str
        return len(league_num_td)

    def parse_match_groups(self, result_str):
        groups_dit = {}
        group_td_list = Selector(text=result_str).xpath("//div[@class='league_num']/table/tr//td")
        print '##################', len(group_td_list)
        for group_td_item in group_td_list:
            group_id = group_td_item.xpath("@id").extract_first()
            groups_dit[group_id] = group_td_item.xpath("a/text()").extract_first()
        return groups_dit

    def parse_match_content_next(self, response):
        match_action_url = 'http://info.sporttery.cn/football/history/action.php'
        print response.body
        sites = {}
        try:
            sites = json.loads(response.body_as_unicode())
        except ValueError:
            print 'Error!!!!!!!'
        response_keys = sites.keys()
        print response_keys
        #解析组类别

        if 'weeks' in response_keys and len(sites['weeks']['result_str'].strip()) > 0:
            weeks_total = self.parse_match_weeks(sites['weeks']['result_str'])
            #获取翻页数据
            groups_dit = {}
            if 'groups' in response_keys:
                groups_dit = self.parse_match_groups(sites['groups']['result_str'])
            else:
                groups_dit['0'] = '0'
            for group_index in groups_dit.keys():
                for page_index in range(1, weeks_total + 1):
                    paramsdit = self.generate_paramsdit(response.meta, 'lc', page_index, group_index)
                    logging.info("请求参数: %s", str(paramsdit))
                    yield FormRequest(match_action_url, meta=response.meta, formdata=paramsdit,
                                      callback=self.parse_match_content, dont_filter=True)
        else:
        # if 'weeks' not in response_keys:
            paramsdit = self.generate_paramsdit(response.meta, 'round')
            print '**********', paramsdit
            yield FormRequest(match_action_url, meta=response.meta, formdata=paramsdit,
                              callback=self.parse_match_content, dont_filter=True)

    def generate_paramsdit(self, meta, action_str, page_index=-1, group_index=0):
        leaguename_season_dit = meta['leaguename_season_dit']
        paramsdit = {}
        if page_index != -1:
            paramsdit['week'] = str(page_index)
        paramsdit['action'] = action_str
        paramsdit['competition_id'] = self.eventid
        paramsdit['c_id'] = self.eventid
        paramsdit['s_id'] = meta['eventid']
        paramsdit['r_id'] = leaguename_season_dit[meta['index']]['id']
        paramsdit['g_id'] = str(group_index)
        paramsdit['table_type'] = 'whole'
        paramsdit['order_type'] = 'all'
        paramsdit['groups'] = leaguename_season_dit[meta['index']]['groups']
        paramsdit['type1'] = 'three_-1_e'
        paramsdit['type2'] = 'asia_229_e'
        paramsdit['round_type'] = leaguename_season_dit[meta['index']]['round_type']
        return paramsdit

    def parse_match_content(self, response):
        sites = json.loads(response.body_as_unicode())
        print sites.keys()
        result_str = sites['matches']['result_str']
        data_table = Selector(text=result_str).xpath("//table[@class='league_data']")
        data_body_tr = data_table.xpath("tr")
        print '!!!!!!!!!!!!!!!!!!', data_body_tr
        for data_body_tr_item in data_body_tr:
            cpmatch_item = self.parse_match_tr(data_body_tr_item, response)
            print cpmatch_item
            yield cpmatch_item

    def parse_match_tr(self, tr_item, response):
        print '@@@@@@@@@@@@@@@@@@@@@@', tr_item.xpath("text()").extract_first()
        data_body_td = tr_item.xpath("td")
        if len(data_body_td) > 0:
            cpmatch_item = CpMatchInfo()
            cpmatch_item['event'] = self.eventid
            cpmatch_item['compsection'] = response.meta['eventname']
            cpmatch_item['compsectionid'] = response.meta['eventid']
            time_str = data_body_td[0].xpath("text()").extract_first()
            if time_str.find("&nbsp ") == -1:
                print '@@@@@@@@@@@@@@@', time_str
                print time_str[0:10], time_str[14:22]
                cpmatch_item['time'] = time_str[0:10] + ' ' + time_str[14:22]
            else:
                cpmatch_item['time'] = time_str.replace("&nbsp ", "")
            cpmatch_item['round'] = data_body_td[1].xpath("text()").extract_first()
            cpmatch_item['hometeamurl'] = data_body_td[2].xpath("a/@href").extract_first()
            cpmatch_item['hometeam'] = data_body_td[2].xpath("a/text()").extract_first()
            cpmatch_item['halfscore'] = data_body_td[3].xpath("text()").extract_first()
            cpmatch_item['totalscore'] = data_body_td[4].xpath("text()").extract_first()
            cpmatch_item['visitteamurl'] = data_body_td[5].xpath("a/@href").extract_first()
            cpmatch_item['visitteam'] = data_body_td[5].xpath("a/text()").extract_first()
            cpmatch_item['awardurl'] = data_body_td[8].xpath("a/@href").extract()[0]
            cpmatch_item['analysisurl'] = data_body_td[8].xpath("a/@href").extract()[1]
            return cpmatch_item
        else:
            return None