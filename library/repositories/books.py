def list_all(conn, available_only=False):
    if available_only:
        return conn.execute("SELECT * FROM books WHERE available = 1").fetchall()
    return conn.execute("SELECT * FROM books").fetchall()


def get(conn, book_id):
    return conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()


def count(conn):
    return conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]


def insert(conn, title, author, isbn):
    cur = conn.execute(
        "INSERT INTO books (title, author, isbn, available) VALUES (?, ?, ?, 1)",
        (title, author, isbn),
    )
    return get(conn, cur.lastrowid)


def delete(conn, book_id):
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))


def set_available(conn, book_id, available):
    conn.execute("UPDATE books SET available = ? WHERE id = ?", (1 if available else 0, book_id))
