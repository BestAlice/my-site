from flask import *
from flask_restful import Resource

class Products(Resource):
    def get(self, product_id):
        #abort_if_news_not_found(news_id)
        self.products = ModelProducts(db.get_connection()).get(news_id)
        return jsonify({'news': news})
 
    def delete(self, news_id):
        #abort_if_product_not_found(product_id)
        ModelProducts(db.get_connection()).delete(news_id)
        return jsonify({'success': 'OK'}) 

class ModelProducts(db.Model): # крректировать
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    group = db.Column(db.String(80), unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
 
    def __repr__(self):
        return #строка

    def abort_if_product_not_found(self, news_id):
       if not ModelProducts(db.get_connection()).get(news_id):
         abort(404, message="News {} not found".format(news_id))