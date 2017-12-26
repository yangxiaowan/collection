# author : YangWan
# -*- coding: utf-8 -*-

from scrapy import Spider


class MatchOddSpider(Spider):

    name = "matchoddspider"

    allowed_domains = "info.sporttery.cn"

    start_urls = [
        "http://info.sporttery.cn/football/info/fb_match_hhad.php"
    ]

    #解析比赛id赔率数组,matchid字段，以逗号分隔
    match_id_list = []

    def __init__(self, category=None, *args, **kwargs):
        super(MatchOddSpider, self).__init__(*args, **kwargs)
        self.match_id_list = kwargs['matchid'].split(",")
        if len(self.match_id_list) == 0:
            raise Exception("参数错误!!!")



