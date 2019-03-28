class BasketModel:
    def __init__(self, connection):
        self.connection = connection

     def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS basket 
                            (product_id INTEGER,
                             buyer_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, product_id, buyer_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO basket
                          (product_id, buyer_id)
                          VALUES (?,?)''', (product_id, buyer_id)
        cursor.close()
        self.connection.commit()

    def get_all(self, buyer_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM basket WHERE buyer_id = ?",
                        (str(user_id)))
        rows = cursor.fetchall()
        return rows

    def delete(self, buyer_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE * FROM basket WHERE buyer_id = ?''',
                         (str(buyer_id)))
        cursor.close()
        self.connection.commit()
    
    def delete_all(self):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE * FROM basket''')
        cursor.close()
        self.connection.commit()