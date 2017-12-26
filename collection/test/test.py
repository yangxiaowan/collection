
# author : YangWan
# -*- coding:utf-8 -*-
from twisted.internet import reactor
from collection.utils import threadmanager
from collection.utils import PropertiesUtil
def funa(*agrs):
    print agrs

def func(agrs):
    print agrs

def funb():
    print 'hello'

def tempfun(fun):
    fun()


class argClass(object):
    def __init__(self):
        self.yangwan = None
        self.wan = None
        self.lan = None
        self.chen = None

    def  setattrs(self, key, value):
        self.__dict__[key] = value

    def printAttr(self):
        print "yangwan", self.yangwan
        print "wan", self.wan
        print "lan", self.lan
        print "chen", self.chen


KEY_AGRS = "yangwan wan lan chen".split()
def agrsFunction(*agrs, **keyAgrs):
    argclass = argClass()
    for agrs in KEY_AGRS:
        temp = "yc_%s" % (agrs,)
        if temp in keyAgrs:
            argclass.setattrs(agrs, keyAgrs[temp])
            del keyAgrs[temp]
    argclass.printAttr()

agrsFunction(yc_wan = "yangwan", yc_lan = "chenlanlan")


# pu = PropertiesUtil.ProertiesUtil()
# print pu.getConfigProperties("mysqldb", "scrapy.db.port")