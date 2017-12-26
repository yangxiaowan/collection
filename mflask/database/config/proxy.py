# author : YangWan
# -- coding: utf-8 --

#数据库代理，动态选择数据库

from mflask import app
from collection.utils.PropertiesUtil import ProertiesUtil
from playhouse.pool import PooledMySQLDatabase

pt = ProertiesUtil("database/database.cfg")
def getDatabaseByCfg(cfgname):
     return PooledMySQLDatabase(
         max_connections=10,
         database = pt.getConfigProperties(cfgname, "scrapy.%s.name" % (cfgname, )),
         passwd = pt.getConfigProperties(cfgname, "scrapy.%s.password" % (cfgname, )),
         user = pt.getConfigProperties(cfgname, "scrapy.%s.user" % (cfgname, )),
         host = pt.getConfigProperties(cfgname, "scrapy.%s.host" % (cfgname, )),
         port = int(pt.getConfigProperties(cfgname, "scrapy.%s.port" % (cfgname, )))
     )

#创建数据库代理,用于选择数据库
# app.config['DEBUG'] = True

#基于应用设置选择数据库代理,返回数据库的代理池
# if app.config['DEBUG']:
#     database = getDatabaseByCfg("testdb")
# elif app.config['TESTING']:
#     database = getDatabaseByCfg("depdb")
# else:
#     database = getDatabaseByCfg("linedb")
database = getDatabaseByCfg("testdb")
database.connect()
print database