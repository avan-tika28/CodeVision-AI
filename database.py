import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# ---------------- USERS TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
email TEXT NOT NULL,
password TEXT NOT NULL
)
""")

# ---------------- PROBLEMS TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS problems(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
difficulty TEXT NOT NULL,
description TEXT NOT NULL,
status TEXT DEFAULT 'Not Solved',
favorite TEXT DEFAULT 'No'
""")

conn.commit()
conn.close()

print("Database Created Successfully!")
