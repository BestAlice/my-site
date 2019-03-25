from flask import *
from flask_restful import reqparse, abort, Api, Resource
from config import *

parser_login = reqparse.RequestParser()
parser_login.add_argument('username', required=True)
parser_login.add_argument('login', required=True)
parser_login.add_argument('password', required=True)
parser_login.add_argument('user_id', required=True, type=int)

class User(Resource): #в помощь
    def get(self):
        news = UserModel(db.get_connection()).get(session['user_id'])
        return jsonify({'users': users})                                                                   
 
    def post(self):
        args = parser.parse_args()
        user = UserModel(db.get_connection())
        user.insert(args['username'], args['password'])
        api.add_resource(user)
        return jsonify({'success': 'OK'})
    
    def delete(self, product_id):
        abort_if_product_not_found(product_id)
        ModelProducts(self.db.get_connection()).delete(product_id)
        return jsonify({'success': 'OK'}) 
        


class UserModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             username VARCHAR(20),
                             password VARCHAR(16),
                             status VARCHAR(16)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (username, password) 
                          VALUES (?,?)''', (user_name, password, 'user'))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row
 
    def exists(self, user_name, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password = ?",
                       (user_name, password))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id)))
        cursor.close()
        self.connection.commit()