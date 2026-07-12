import sqlite3
import csv

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

with open("data/problems.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute("""
            INSERT OR IGNORE INTO problems
            (title, difficulty, description, status, favorite)
            VALUES (?, ?, ?, ?, ?)
        """, (
            row["title"],
            row["difficulty"],
            row["description"],
            "Not Solved",
            "No"
        ))

conn.commit()
conn.close()

print("✅ Problems imported successfully!")