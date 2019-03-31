from db_connect import DB
import sqlite3

class ProductModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(50),
                             content VARCHAR(200),
                             price VARCHAR(10),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, price, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO products 
                          (title, content, price, user_id) 
                          VALUES (?,?,?,?)''', (title, content, price, str(user_id)))
        cursor.close()
        self.connection.commit()

    def get(self, produscs_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (str(produscs_id)))
        row = cursor.fetchone()
        return row
 
    def get_all(self, user_id = None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM products WHERE user_id = ?",
                           (str(user_id)))
        else:
            cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        return rows

    def delete(self, produscs_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM products WHERE id = ?''', (str(produscs_id)))
        cursor.close()
        self.connection.commit()

    def delete_with_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM products WHERE user_id = ?''',
                         (str(user_id)))
        cursor.close()
        self.connection.commit()