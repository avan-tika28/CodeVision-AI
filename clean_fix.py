import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Keep only unique titles
cursor.execute("""
DELETE FROM problems
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM problems
    GROUP BY title
)
""")

conn.commit()
conn.close()

print("✅ Duplicates removed successfully")