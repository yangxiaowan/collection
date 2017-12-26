# author : YangWan
# -*- coding:utf-8 -*-
from twisted.internet import reactor
import time

class threadmanager:
    '线程管理'

    def __init__(self):
        print 'init'

    #更改线程池大小
    def changeThreadPoolSize(self, poolsize=10):
        reactor.suggestThreadPoolSize(poolsize)

    def executeFunction(self, callFunction):
        print 'executeFunction running!!!'
        reactor.callInThread(callFunction)
        reactor.run()

    def executeMutiplyFunction(self, callFunction, commandList):
        reactor.callMultipleInThread(commandList)
        reactor.run()



