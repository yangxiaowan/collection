
from flask import Flask
from mflask.database.config.proxy import database
from mflask.test import testflask
from mflask.app import fivelotterydbinfo


app = Flask(__name__)


app.register_blueprint(testflask.mod)
app.register_blueprint(fivelotterydbinfo.mod)


@app.before_request
def get_db_connection():
    database.connect()
