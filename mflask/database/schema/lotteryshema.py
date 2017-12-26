# author : YangWan
# -- coding: utf-8 --
"""
    对象序列化成json模板，采用marshmallow进行json序列化
"""
from marshmallow import Schema
from marshmallow import fields
from mflask.database.model.model import kjlottery

class KjlotterySchema(Schema):
    id = fields.Integer()
    product = fields.Str()
    lotterytype = fields.Str()
    lottno = fields.Str()
    kjnum = fields.Str()
