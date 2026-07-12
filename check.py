import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM problems")
print("Total:", cursor.fetchone()[0])

conn.close()