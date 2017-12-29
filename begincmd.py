# author : YangWan
# coding: utf-8

from scrapy import cmdline
cmdline.execute("scrapy crawl qmcbaiduspider -a category=baidu -a keyword=全民彩票 -a pagenum=100".split())
import thread

# def execute500LotteryScrapy():
#     cmdline.execute("scrapy crawl lottscra".split())

# def executeZgzcwScrapy():
#     cmdline.execute("scrapy crawl zgzcwspider".split())
#
# executeZgzcwScrapy()

#将参数53510492穿入spider中作为参数
# cmdline.execute("scrapy crawl lottscra".split())

#http://zx.500.com/zqdc/shuju.php?pt=1&mc=82&bt=2007-11-1&et=2017-11-28&rq=&tm=0
# cmdline.execute("scrapy crawl caikespider -a pt_params=1 -a mc_params=82 -a bt_params=2007-11-1 -a et_params=2017-11-28 -a rq_params= -a tm_params=0".split())

# http://zx.500.com/zqdc/inc/shuju_saishi.php?gt=ajax&pn=2&pt=2&mc=82&bt=2007-11-1&et=2017-11-28&rq=&tm=0
# cmdline.execute("scrapy crawl matchhistoryspider -a pn_params=1 -a pt_params=2 -a mc_params=82 -a bt_params=2007-11-1"\
#                 " -a et_params=2017-11-28 -a rq_params= -a tm_params=0".split())

# m_list = [1, 2, 3, 4]
# cmdline.execute("scrapy crawl cpmatchhistoryspider -a ]
# cmdline.execute("scrapy crawl cpfootballspider".split())

# cmdline.execute("scrapy crawl cpmatchhistoryspider -a eventid=1129 -a matchid=".split())
# cmdline.execute("scrapy crawl cpmatchhistoryspider -a eventid=1076 -a matchid=".split())
cmdline.execute("scrapy crawl qmcbaiduspider -a category=baidu -a keyword=全民彩票 -a pagenum=100".split())
