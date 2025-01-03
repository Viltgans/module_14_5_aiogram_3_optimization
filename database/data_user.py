import sqlite3

def initiate_user_db():
    connect2 = sqlite3.connect('database/users.db')
    cursor2 = connect2.cursor()

    cursor2.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL DEFAULT 1000
    );
    ''')

    connect2.commit()
    connect2.close()

def add_user(username, email, age):
    connect2 = sqlite3.connect('database/users.db')
    cursor2 = connect2.cursor()
    cursor2.execute("INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)",
                   (f'{username}', f'{email}', f'{age}', 1000))
    connect2.commit()
    connect2.close()

def is_included(username):
    connect2 = sqlite3.connect('database/users.db')
    cursor2 = connect2.cursor()
    user = cursor2.execute('SELECT * FROM Users WHERE username = ?', (username,)).fetchone()
    connect2.commit()
    connect2.close()
    return user is not None