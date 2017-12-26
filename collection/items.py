# author : YangWan
# -*- coding: utf-8 -*-

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DmozItem(scrapy.Item):
    title = scrapy.Field()

class LottKjItem(scrapy.Item):
    product = scrapy.Field()
    lotterytype = scrapy.Field()
    lottno = scrapy.Field()
    kjnum = scrapy.Field()

class FootballSfcItem(scrapy.Item):
    expect = scrapy.Field()  #胜负彩期数
    updatetime =  scrapy.Field() #胜负彩更新日期

#足彩网开奖信息爬取信息结果
class ZgzcwItem(scrapy.Item):
    classification = scrapy.Field()
    lotterytype = scrapy.Field()
    period = scrapy.Field()
    kjresult = scrapy.Field()
    kjtime = scrapy.Field()

class MatcherData(scrapy.Item):
    eventtype = scrapy.Field() #赛事类型
    matchertime = scrapy.Field() #比赛时间
    hometeam = scrapy.Field() #主队
    letball = scrapy.Field() #让球
    visitingteam = scrapy.Field() #客队
    score = scrapy.Field() #比分
    collection = scrapy.Field() #彩果
    collectionsp = scrapy.Field() #开奖sp
    compensatewin = scrapy.Field() #胜场欧赔
    compensateflat = scrapy.Field() #平场欧赔
    compensatenegative = scrapy.Field() #负场欧赔

#爬取网站http://info.sporttery.cn/football/history/data_center.php
#中国竞彩网赛事类别分别
class EventType(scrapy.Item):
    eventid = scrapy.Field()  #比赛对应id
    eventyclass = scrapy.Field() #赛事类型
    eventcountry = scrapy.Field() #国家比赛
    event = scrapy.Field() #赛事

#中国竞彩信息网的历史赛果
class CpMatchInfo(scrapy.Item):
    event = scrapy.Field() #赛事
    compsection = scrapy.Field() #赛季
    compsectionid = scrapy.Field() #赛季编号
    time = scrapy.Field() #比赛时间
    round = scrapy.Field() #轮次
    hometeam = scrapy.Field() #主队
    halfscore = scrapy.Field() #半场比分
    totalscore = scrapy.Field() #全场比分
    visitteam = scrapy.Field() #客队
    hometeamurl = scrapy.Field() #主队分析url
    visitteamurl = scrapy.Field() #客队分析url
    awardurl = scrapy.Field() #奖url
    analysisurl = scrapy.Field() #析url

class XiciFreeIp(scrapy.Item):
    country = scrapy.Field() #国家
    ipstr = scrapy.Field() #ip
    port = scrapy.Field() #端口
    serverlocal = scrapy.Field() #服务器地址
    ishide = scrapy.Field() #是否高匿
    httptype = scrapy.Field() #请求类型
    speed = scrapy.Field() #速度
    connecttime = scrapy.Field() #连接时间
    alivetime = scrapy.Field() #存活时间
    verifytime = scrapy.Field() #验证时间
    lastupdate = scrapy.Field() #入库时间

class QmcSeachItem(scrapy.Item):
    rankindex = scrapy.Field() #搜索排名
    websiteurl = scrapy.Field() #网站链接
    pageurl = scrapy.Field() #图片链接地址
    seachdesc = scrapy.Field() #搜索基础内容描述
    seachtitle =scrapy.Field() #搜索主题
    type = scrapy.Field() #搜索类型 有词条和广告两种

class RelevantSearchItem(scrapy.Item):
    keyword = scrapy.Field() #关键字
    recommendword = scrapy.Field() #推荐搜索
    relevantword = scrapy.Field() #相关搜索
