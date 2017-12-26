# author : YangWan
# -*- coding: utf-8 -*-
from flask import abort
from flask import redirect
from flask import Blueprint


mod = Blueprint('test', __name__, url_prefix='/test')

@mod.route('/mod')
def index():
    return '<h1>Hello World!</h1>'

@mod.route('/user/<name>')
def sayHello(name):
    if name == 'baidu':
        return redirect('http://www.baidu.com')
    elif name == 'NO':
        return abort(404)

    return '<h1> Hello,%s </h1>' % name