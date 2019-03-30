from db_connect import DB
import sqlite3

class BasketModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS basket 
                            (product_id INTEGER,
                             buyer_id INTEGER,
                             seller_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, product_id, buyer_id, seller_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO basket
                          (product_id, buyer_id, seller_id)
                          VALUES (?,?,?)''', (product_id, buyer_id, seller_id))
        cursor.close()
        self.connection.commit()

    def get(self, product_id, buyer_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM basket WHERE buyer_id = ?",
                        (str(buyer_id)))
        rows = cursor.fetchall()
        return rows

    def get_all(self, buyer_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT product_id, seller_id FROM basket WHERE buyer_id = ?",
                        (str(buyer_id)))
        rows = cursor.fetchall()
        return rows

    def delete_one(self, product_id, buyer_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM basket WHERE product_id = ? and buyer_id = ?''',
                         (str(product_id), str(buyer_id)))
        cursor.close()
        self.connection.commit()
    
    def delete_for_buyer(self, buyer_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM basket WHERE buyer_id = ?''',
                         (str(buyer_id)))
        cursor.close()
        self.connection.commit()
    
    def delete_with_seller(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM basket WHERE seller_id = ?''',
                         (str(user_id)))
        self.delete_for_buyer(user_id)
        cursor.close()
        self.connection.commit()
    
    def delete_with_product(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM basket WHERE product_id = ?''', 
                          (str(product_id)))
        cursor.close()
        self.connection.commit()