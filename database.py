import sqlite3
import os

DATABASE = 'wishlist.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # ↓↓↓ ЭТИ ДВЕ СТРОЧКИ УДАЛЯЮТ СТАРУЮ БАЗУ ДАННЫХ ↓↓↓
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    # ↑↑↑ ЭТИ ДВЕ СТРОЧКИ УДАЛЯЮТ СТАРУЮ БАЗУ ДАННЫХ ↑↑↑
    
    conn = get_db()
    conn.execute('''
        CREATE TABLE wishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            link TEXT,
            status TEXT CHECK(status IN ('pending', 'completed')) DEFAULT 'pending'
        )
    ''')
    # Демо-данные в рублях
    conn.execute('INSERT INTO wishes (name, price, link, status) VALUES (?, ?, ?, ?)',
                 ('Наушники Sony', 12000.0, 'https://example.com', 'pending'))
    conn.execute('INSERT INTO wishes (name, price, link, status) VALUES (?, ?, ?, ?)',
                 ('Книга по Flask', 3500.0, '', 'completed'))
    conn.commit()
    conn.close()
