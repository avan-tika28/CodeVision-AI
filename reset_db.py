import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS problems")

cursor.execute("""
CREATE TABLE problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    difficulty TEXT,
    description TEXT,
    status TEXT,
    favorite TEXT
)
""")

conn.commit()
conn.close()

print("DB reset done")