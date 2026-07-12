import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

try:
    cursor.execute(
        "ALTER TABLE problems ADD COLUMN favorite TEXT DEFAULT 'No'"
    )

    print("Favorite column added successfully!")

except sqlite3.OperationalError:
    print("Favorite column already exists!")

conn.commit()
conn.close()