from flask import *
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

parser = reqparse.RequestParser()
#parser.add_argument('title', required=True)
#parser.add_argument('content', required=True)
#parser.add_argument('user_id', required=True, type=int)

def abort_if_news_not_found(news_id):
    if not NewsModel(db.get_connection()).get(news_id):
        abort(404, message="News {} not found".format(news_id))

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')