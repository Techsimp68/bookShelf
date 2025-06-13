# test_db.py

import sqlite3

# Path to your database
DB_PATH = "backend/python/database/bookstore.db"

def insert_and_fetch_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Insert test user, book, and chapter
    cur.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", ("test_user",))
    cur.execute("INSERT OR IGNORE INTO books (title, author) VALUES (?, ?)", ("Test Book", "Test Author"))
    conn.commit()

    # Get inserted user and book ID
    cur.execute("SELECT id FROM users WHERE username = ?", ("test_user",))
    user_id = cur.fetchone()[0]

    cur.execute("SELECT id FROM books WHERE title = ?", ("Test Book",))
    book_id = cur.fetchone()[0]

    # Insert chapter
    cur.execute("""
        INSERT INTO chapters (book_id, chapter_number, content, is_dynamic)
        VALUES (?, ?, ?, ?)
    """, (book_id, 1, "This is a test chapter content.", False))
    conn.commit()

    # Fetch and print data for video demonstration
    print(" Users:")
    for row in cur.execute("SELECT * FROM users"):
        print(row)

    print("\n Books:")
    for row in cur.execute("SELECT * FROM books"):
        print(row)

    print("\n Chapters:")
    for row in cur.execute("SELECT * FROM chapters"):
        print(row)

    conn.close()

if __name__ == "__main__":
    insert_and_fetch_data()