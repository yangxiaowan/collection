# author : YangWan
# coding: utf-8
import os
# class Chain(object):
#
#     def __init__(self, path=''):
#         self._path = path
#
#     def __getattr__(self, path):
#         return Chain('%s/%s' % (self._path, path))
#
#     def __str__(self):
#         return self._path
#
# chain = Chain()
# print chain.status
# #每次点调用属性都会自动调用__getattr__方法
# print Chain().status.user.timeline.list
print "the current pwd is %s" % os.getcwd()
print "the current thread is %s" % os.getpid()
pid = os.fork()
if pid == 0:
    print 'I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid())
else:
    print 'I (%s) just created a child process (%s).' % (os.getpid(), pid)
