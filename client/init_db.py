import sqlite3

conn = sqlite3.connect("linechat.db")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, signed_in INTEGER)")

conn.close()