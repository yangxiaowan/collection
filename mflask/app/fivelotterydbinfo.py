# author : YangWan
# -- coding: utf-8 --
from flask import request
from flask import Blueprint
from mflask.database.model.model import kjlottery
from mflask.database.schema.lotteryshema import KjlotterySchema

from collection.utils.workutils import hasParams
from flask import jsonify

#获得500彩票网数据库中的相关信息
mod = Blueprint('fivelotterydb', __name__, url_prefix='/fivelotterydb')

#获得数据库中所有的开奖信息
@mod.route('/getallkjinfo', methods = ['GET'])
def getallkjinfo():
    kjino = kjlottery.select().where(kjlottery.id == 91).get()
    schema = KjlotterySchema()
    kjentity = schema.dump(kjino)
    print kjentity.data
    return jsonify(kjentity.data)

#按条件查询开奖信息，这是按主键进行查询,参数提交方式POST
#参数product -- lotterytype -- lottno
#product="竞技"&lotterytype="胜负彩(任9)"&lottno="17173"
#通过request.args来获取get方法提交的参数,通过request.form来获得post提交的参数
@mod.route('/getkjinfobyperiod', methods = ['GET'])
def getkjinfobyperiod():
    print request.args['product']
    product_cdt = request.args['product']
    lotterytype_cdt = request.form['lotterytype']
    lottno_cdt = request.form['lottno']
    print "the params: ", product_cdt, lotterytype_cdt, lottno_cdt
    return "Hello"
    query = kjlottery.select()
    if hasParams(product_cdt):
        query.where(kjlottery.product == product_cdt)
    if hasParams(lotterytype_cdt):
        query.where(kjlottery.lotterytype == lotterytype_cdt)
    if hasParams(lottno_cdt):
        query.where(kjlottery.lottno == lottno_cdt)
    conditionQuery = query.get()
    schema = KjlotterySchema()
    kjentity = schema.dump(conditionQuery)
    print kjentity.data
    return jsonify(kjentity.data)

@mod.route('getkjinofbylotterytype', methods = ['POST'])
def getkjinofbylotterytype():
    pass

#获得数据库中开奖信息的总条数
@mod.route('/getallnum')
def getallnum():
    return kjlottery.select()



