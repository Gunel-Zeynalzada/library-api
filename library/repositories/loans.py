def list_all(conn):
    return conn.execute("SELECT * FROM loans").fetchall()


def get(conn, loan_id):
    return conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()


def for_member(conn, member_id):
    return conn.execute("SELECT * FROM loans WHERE member_id = ?", (member_id,)).fetchall()


def insert(conn, book_id, member_id, due_date, checked_out):
    cur = conn.execute(
        "INSERT INTO loans (book_id, member_id, due_date, checked_out) VALUES (?, ?, ?, ?)",
        (book_id, member_id, due_date, checked_out),
    )
    return get(conn, cur.lastrowid)


def mark_returned(conn, loan_id, fine):
    conn.execute("UPDATE loans SET returned = 1, fine = ? WHERE id = ?", (fine, loan_id))
    return get(conn, loan_id)


def extend(conn, loan_id, new_due_date):
    conn.execute(
        "UPDATE loans SET due_date = ?, renewals = renewals + 1 WHERE id = ?",
        (new_due_date, loan_id),
    )
    return get(conn, loan_id)


def mark_fine_paid(conn, loan_id):
    conn.execute("UPDATE loans SET fine_paid = 1 WHERE id = ?", (loan_id,))
    return get(conn, loan_id)


def open_with_details(conn):
    """Unreturned loans joined with book title and member name (for reports)."""
    return conn.execute(
        """
        SELECT loans.id AS loan_id, books.title AS title,
               members.name AS member, loans.due_date AS due_date
        FROM loans
        JOIN books ON books.id = loans.book_id
        JOIN members ON members.id = loans.member_id
        WHERE loans.returned = 0
        """
    ).fetchall()
