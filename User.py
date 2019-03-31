from db_connect import DB
import sqlite3

class UserModel:

    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(16),
                             password_hash VARCHAR(16),
                             status VARCHAR(10),
                             buy INTEGER,
                             sale INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, status, buy, sale):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, status, buy, sale) 
                          VALUES (?,?,?,?,?)''', 
                          (user_name, password_hash, status, buy, sale))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row
 
    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def new_buy(self, user_id, len_products=1):
        cursor = self.connection.cursor()
        buy = self.get(user_id)[4] + len_products
        cursor.execute('''UPDATE users SET buy = ? WHERE id = ?''',(str(buy),str(user_id)))
        cursor.close()
        self.connection.commit()
    
    def new_sale(self, user_id):
        cursor = self.connection.cursor()
        sale = self.get(user_id)[5] + 1
        cursor.execute('''UPDATE users SET sale = ? WHERE id = ?''',(str(sale),str(user_id)))
        cursor.close()
        self.connection.commit()

    def delete_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''',
                         (str(user_id)))
        cursor.close()
        self.connection.commit()
    
    def do_admin(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users SET status = ? WHERE id = ?''',('admin', str(user_id)))
        cursor.close()
        self.connection.commit()