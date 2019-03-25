from flask import *
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import *

#self.id_prod, self.name, self.text, self.user_id, self.user
parser_login = reqparse.RequestParser()
parser_login.add_argument('id_prod', required=True, type=int)
parser_login.add_argument('title', required=True)
parser_login.add_argument('password', required=True)
parser_login.add_argument('user_id', required=True, type=int)

def abort_if_product_not_found(self, product_id):
    if not ModelProducts(db.get_connection()).get(product_id):
        abort(404, message="Product {} not found".format(product_id))

class ModelProducts(db.Model): # корректировать
    global db
    id_prod = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    text = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer,
                           db.ForeignKey('yandex_lyceum_student.id'),
                           nullable=False)
    user = db.relationship('User',
                            backref=db.backref('ModelProducts',
                            lazy=True))
 
    def __repr__(self):
        return '<ModelProducts {} {} {}>'.format(
            self.id_prod, self.title, self.text, self.user_id, self.user)

class Products(Resource): 
    def __init__(self, db):
        self.db = db 

    def get(self, product_id):
        abort_if_product_not_found(product_id)
        products = ModelProducts(self.db.get_connection()).get(product_id)
        return jsonify({'products': products})
 
    def delete(self, product_id):
        abort_if_product_not_found(product_id)
        ModelProducts(self.db.get_connection()).delete(product_id)
        return jsonify({'success': 'OK'}) 