import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
DELETE FROM problems
WHERE id NOT IN (
    SELECT MIN(id)
    FROM problems
    GROUP BY title
)
""")

conn.commit()

cursor.execute("SELECT COUNT(*) FROM problems")
print("Remaining Problems:", cursor.fetchone()[0])

conn.close()