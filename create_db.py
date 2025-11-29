import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        title TEXT,
        applicant TEXT,
        issue_date TEXT,
        status TEXT,
        pdf_path TEXT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        username TEXT PRIMARY KEY,
        password TEXT
    )
""")

# default admin (change password in instance/config.json later)
try:
    cur.execute("INSERT OR IGNORE INTO admins (username, password) VALUES (?, ?)", ('admin', 'admin123'))
except Exception as e:
    print('Admin insert error:', e)

conn.commit()
conn.close()
print('Database initialized at', DB_PATH)
