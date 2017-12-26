# author : YangWan
from twisted.internet import reactor
from twisted.internet.defer import Deferred

def getdata(val_num):
    print "this val_num :" + str(val_num)

def product_data():
    print 'couting!!!'
    for num in range(10, 20):
        print 'couting as!!!'
        getdata(num)

reactor.callWhenRunning(product_data)
print 'starting reactor!!!'
reactor.run()
