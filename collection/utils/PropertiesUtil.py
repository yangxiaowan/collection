# author : YangWan
# -- coding: utf-8 --

import ConfigParser

class ProertiesUtil:


    #读取配置文件
    def __init__(self, filename= "..\\..\\scrapy.cfg"):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read(filename)

    #重置配置文件路径
    def getConfigFile(self, filename):
        self.conf.read(self.filename)

    #根据键值获得配置文件分类下的配置value
    def getConfigProperties(self, classification, keyname):
        return self.conf.get(classification, keyname)



