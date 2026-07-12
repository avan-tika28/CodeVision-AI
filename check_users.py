import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

print("=== USERS TABLE STRUCTURE ===")
cursor.execute("PRAGMA table_info(users)")
for row in cursor.fetchall():
    print(row)

print("\n=== USERS DATA ===")
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(row)

conn.close()