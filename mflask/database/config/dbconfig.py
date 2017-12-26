# author : YangWan
# -- coding: utf-8 --
from peewee import *
from flask import jsonify
from mflask.database.config.proxy import database
from mflask.database.schema.lotteryshema import KjlotterySchema
# host = 'localhost'
# database = MySQLDatabase(
#     database = 'scrapydb',
#     passwd = 'beyonddream',
#     user = 'root',
#     host = host,
#     port = 3306,
# )
# print database
database.connect()
print database.get_conn()

class BaseModel(Model):
    class Meta:
        database = database
class kjzgzcw(BaseModel):
    classification = CharField()
    lotterytype = CharField()
    period = CharField()
    kjresult = CharField()
    kjtime = CharField()

class kjlottery(BaseModel):
    id = IntegerField()
    product = CharField()
    lotterytype = CharField()
    lottno = CharField()
    kjnum = CharField()

temp = kjlottery.select().where(kjlottery.id == 91).get()
schema = KjlotterySchema()
kjentity = schema.dump(temp)
print kjentity.data


for tempkj in kjlottery.select():
    print tempkj.kjnum