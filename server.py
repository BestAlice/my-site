from flask import *
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from main_list import Mein_list
#from werkzeug.security import generate_password_hash

# ПОМОГИТЕЕЕЕЕЕЕЕЕЕЕ.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
#hash = generate_password_hash('yandexlyceum')

parser_login = reqparse.RequestParser()
parser_login.add_argument('name', required=True)
parser_login.add_argument('login', required=True)
parser_login.add_argument('password', required=True)
parser_login.add_argument('user_id', required=True, type=int)

api.add_resource(Main_list , '/')

#def abort_if_news_not_found(news_id):
 ##   if not NewsModel(db.get_connection()).get(news_id):
 #      abort(404, message="News {} not found".format(news_id))

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')