import sqlite3
import generater

conn = sqlite3.connect('database.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username text, email text, password text, address text)''')
conn.commit()
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS product (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, price INTEGER)''')
conn.commit()
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id text, product_name text, count INTEGER, total_amount INTEGER)''')
conn.commit()

for _ in range(1000):
    user = generater.generate_user() + (generater.generate_address(), )
    c.execute('INSERT INTO users(username, email, password, address) VALUES(?,?,?,?)', user)

keywords = ['컴퓨터','헤드셋','무선이어폰','마우스','키보드']
product_list = []

for keyword in keywords:
    for product in generater.generate_product(keyword):
        c.execute('INSERT INTO product(name, price) VALUES(?,?)', (product['name'],product['price']))

conn.commit()
