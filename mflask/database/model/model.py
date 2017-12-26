# author : YangWan
# -- coding: utf-8 --
from peewee import *
from mflask import database as lotterydb

class BaseModel(Model):

    class Meta:
        database = lotterydb

class kjlottery(BaseModel):
    id = IntegerField()
    product = CharField()
    lotterytype = CharField()
    lottno = CharField()
    kjnum = CharField()


class kjzgzcw(BaseModel):
    classification = CharField()
    lotterytype = CharField()
    period = CharField()
    kjresult = CharField()
    kjtime = CharField()

class test(BaseModel):
    name = CharField()


# grandma = kjlottery.select().where(kjlottery.id == 91).get()
# tempstr = test.select()
# print tempstr
# tempstr = test.create(name="lanlan", id = 232)
# for temp in test.select():
#     print temp.name