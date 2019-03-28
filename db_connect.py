import sqlite3
 
 
class DB:
    def __init__(self):
        conn = sqlite3.connect('base.db', check_same_thread=False)
        self.conn = conn
 
    def get_connection(self):
        return self.conn
 
    def __del__(self):
        self.conn.close()

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
                             basket 
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, status):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, status) 
                          VALUES (?,?,?)''', (user_name, password_hash, status))
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