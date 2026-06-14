import sqlite3
import os

DATABASE = 'wishlist.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('DROP TABLE IF EXISTS wishes')
    conn.execute('''
        CREATE TABLE wishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            link TEXT,
            status TEXT CHECK(status IN ('pending', 'completed')) DEFAULT 'pending'
        )
    ''')
    conn.execute("INSERT INTO wishes (name, price, link, status) VALUES (?, ?, ?, ?)",
                 ('Alan Wake 2', 12000, '', 'pending'))
    conn.execute("INSERT INTO wishes (name, price, link, status) VALUES (?, ?, ?, ?)",
                 ('Resident Evil Requiem', 3500, '', 'completed'))
    conn.commit()
    conn.close()
