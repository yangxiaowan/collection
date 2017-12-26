import threading
import time
import random
from multiprocessing import Process, Queue

# def printHello(valueName):
#     time.sleep(1)
#     print valueName
#     print 'hello world!!!'

# for i in range(5):
#     thread = threading.Thread(target=printHello)
#     thread.start()
#     thread.join()

# if __name__=='__main__':
#     p = Process(target=printHello, args=('test!!', ))
#     p.start()
#     p.join()
#     print 'END'

def writeBuff(queue):
    for chartemp in ['A', 'B', 'C', 'D']:
        print 'put the %s to queue', chartemp
        queue.put(chartemp)
        time.sleep(random.random())

def readBuffer(queue):
    while True:
        value =  queue.get(True)
        print 'Get %s from queue.' % value

if __name__ == '__main__':
    queue = Queue()
    writeThread = Process(target=writeBuff, args=(queue, ))
    readThread = Process(target=readBuffer, args=(queue, ))
    writeThread.start()
    readThread.start()
    writeThread.join()
    print 'Threading End'





