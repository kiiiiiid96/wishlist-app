cat > database.py << 'EOF'
import sqlite3
import os

DATABASE = 'wishlist.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    
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
    conn.execute("INSERT INTO wishes (name, price, link, status) VALUES (?, ?, ?, ?)",
                 ('Halloween: The Game', 1500.0, '', 'pending'))
    conn.execute("INSERT INTO wishes (name, price, link, status) VALUES (?, ?, ?, ?)",
                 ('SILENT HILL: Townfall', 4000.0, '', 'completed'))
    conn.commit()
    conn.close()
    print("✅ База создана с рублями!")
EOF
