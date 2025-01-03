import sqlite3

def initiate_product_db():
    connect = sqlite3.connect('database/products.db')
    cursor = connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Products(id INT); ")

def get_all_products():
    connect = sqlite3.connect('database/products.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connect.commit()
    connect.close()
    return products