# author : YangWan
# -*- coding: utf-8 -*-

from collection.utils import PropertiesUtil
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
import logging
from collection.items import EventType

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

#Twisted.enterprise 数据库支持服务
#Twisted是用python实现的基于事件驱动的网络引擎框架，使用 adbapi.ConnectionPool 类来管理连接
#这样可以使用adbapi来使用多个连接，比如一个线程一个连接
#数据库连接Pipeline
#专门用来处理直接存储item对象
class MySQLPipeline(object):

    propertiesUtil = PropertiesUtil.ProertiesUtil()

    def __init__(self):
        #获取数据库配置信息
        # self.dbport = self.propertiesUtil.getConfigProperties("mysqldb", "scrapy.db.port")
        # self.dbuser = self.propertiesUtil.getConfigProperties("mysqldb", "scrapy.db.user")
        # self.dbhost = self.propertiesUtil.getConfigProperties("mysqldb", "scrapy.db.host")
        # self.dbpassword = self.propertiesUtil.getConfigProperties("mysqldb", "scrapy.db.password")
        # self.dbname = self.propertiesUtil.getConfigProperties("mysqldb", "scrapy.db.name")
        self.dbpool = adbapi.ConnectionPool("MySQLdb",
                                           db = "scrapydb",
                                           host = "127.0.0.1",
                                           user = "root",
                                           passwd = "beyonddream",
                                           cursorclass = MySQLdb.cursors.DictCursor,
                                           charset = "utf8",
                                           use_unicode = True)

    # pipeline默认调用
    def process_item(self, item, spider):
        if spider.name == 'lottscra':
            query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        elif spider.name == 'zgzcwspider':
            print "zgzcwspider result to mysql!!!!!!!"
            query = self.dbpool.runInteraction(self._conditional_insert_zgzcw, item)
        elif spider.name == 'matchhistoryspider':
            logging.info("matchhistoryspider result to mysql!")
            query = self.dbpool.runInteraction(self._conditional_insert_matchhistory, item)
        elif spider.name == 'cpfootballspider':
            logging.info("cpfootballspider result to mysql!")
            if type(item) == EventType:
                query = self.dbpool.runInteraction(self._conditional_insert_matcheventtype, item)
        elif spider.name == 'cpmatchhistoryspider':
            logging.info("cpmatchhistoryspider result to mysql!")
            query = self.dbpool.runInteraction(self._conditional_insert_cpmatchhistory, item)
        elif spider.name == 'xicidailispider':
            logging.info("xicidailispider result to mysql!")
            query = self.dbpool.runInteraction(self._conditional_insert_xicidailispider, item)
        else:
            return None
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    def _conditional_insert_matcheventtype(self, tx, item):
        sql = "insert into eventtype(eventid, event, eventyclass, eventcountry) values(%s,%s,%s,%s)"
        params = (item["eventid"], item["event"], item["eventyclass"], item["eventcountry"])
        print params
        tx.execute(sql, params)

    def _conditional_insert_cpmatchhistory(self, tx, item):
        sql = "insert into cpmatchhistory(event, compsection, compsectionid, time, round, hometeam, halfscore," \
              "totalscore, visitteam, hometeamurl, visitteamurl, awardurl, analysisurl)" \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item["event"], item["compsection"], item["compsectionid"], item["time"], item["round"], \
                  item["hometeam"], item["halfscore"], item["totalscore"], item["visitteam"], \
                  item["hometeamurl"], item["visitteamurl"], item["awardurl"], item["analysisurl"])
        logging.info("save data: %s", params)
        tx.execute(sql, params)

    def _conditional_insert_xicidailispider(self, tx, item):
        sql = "insert into xicifreeip(ipstr, country, port, serverlocal, ishide, httptype, speed," \
              "connecttime, alivetime, verifytime, lastupdate)" \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item["ipstr"], item["country"], item["port"], item["serverlocal"], item["ishide"], \
                  item["httptype"], item["speed"], item["connecttime"], item["alivetime"], \
                  item["verifytime"], item["lastupdate"])
        logging.info("save data: %s", params)
        tx.execute(sql, params)

    #将历史比赛信息导入数据库
    def _conditional_insert_matchhistory(self, tx, item):
        sql = "insert into matchhistory(eventtype, matchertime, hometeam, letball, visitingteam, score, collection," \
            "collectionsp, compensatewin, compensateflat, compensatenegative) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item["eventtype"], item["matchertime"], item["hometeam"], item["letball"], item["visitingteam"], \
                  item["score"], item["collection"], item["collectionsp"], item["compensatewin"],\
                  item["compensateflat"], item["compensatenegative"])
        logging.info("save data: %s", params)
        tx.execute(sql, params)

    #将足彩网开奖结果入库
    def _conditional_insert_zgzcw(self, tx, item):
        sql = "insert into kjzgzcw(classification, lotterytype, period, kjresult, kjtime) values(%s,%s,%s,%s,%s)"
        params = (item["classification"], item["lotterytype"], item["period"], item["kjresult"], item["kjtime"])
        print params
        tx.execute(sql, params)

    #写入数据到数据库
    def _conditional_insert(self, tx, item):
        sql = "insert into kjlottery(product,lotterytype, lottno, kjnum) values(%s,%s,%s,%s)"
        params = (item["product"], item["lotterytype"], item["lottno"], item["kjnum"])
        tx.execute(sql, params)

    #错误处理方法
    def _handle_error(self, failue, item, spider):
        print '--------------database operation exception!!-----------------'
        print '-------------------------------------------------------------'
        print failue
