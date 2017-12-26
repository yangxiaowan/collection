# author : YangWan
# -*- coding:utf-8 -*-

import urllib
import urllib2

#python 发送get请求
# url = "http://www.310win.com/Info/Result/Soccer.aspx?load=ajax&typeID=1&IssueID=1852373"
# req = urllib2.Request(url)
# print req
# res_data = urllib2.urlopen(req)
# res = res_data.read()
# print res

class A(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        print self.name, self.value, "A object __init__"
    def connect(self):
        super(A, self).connect()
        print "A connect"
class B(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        print self.name, self.value, "B object __init__"
    def connect(self):
        print "B connect"
class C(A, B):
    pass

c = C("yanwan", 22)
print C.mro()
c.connect()