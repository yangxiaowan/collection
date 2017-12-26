# author : YangWan
# -*- coding:utf-8 -*-
import threading
kuaizi = 1
daocha = 1

def getKuaizi():
    global kuaizi
    while True:
        if(kuaizi == 1):
            kuaizi -= 1
            break

def backKuaizi():
    global kuaizi
    kuaizi += 1

def getDaocha():
    global daocha
    while True:
        if(daocha == 1):
            daocha -= 1
            break

def backDaocha():
    global daocha
    daocha += 1

kuaiziLock = threading.Lock()
daochaLock = threading.Lock()

def xiaoming():
    try:
        kuaiziLock.acquire()
        getKuaizi()
        kuaiziLock.release()
        daochaLock.acquire()
        getDaocha()
        daochaLock.release()
    finally:
        print "xiaoming eating!!!!"


def xiaohong():
    try:
        kuaiziLock.acquire()
        getKuaizi()
        kuaiziLock.release()
        daochaLock.acquire()
        getDaocha()
        daochaLock.release()
    finally:
        print "xiaohong eating!!!!"

xiaomingThread = threading.Thread(target=xiaoming, name='xiaomingThread')
xiaohongThread = threading.Thread(target=xiaohong, name='xiaohongThread')
xiaomingThread.start()
xiaohongThread.start()
xiaomingThread.join()
xiaohongThread.join()
