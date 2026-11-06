def list_all(conn):
    return conn.execute("SELECT * FROM members").fetchall()


def get(conn, member_id):
    return conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()


def get_by_email(conn, email):
    return conn.execute("SELECT * FROM members WHERE email = ?", (email,)).fetchone()


def insert(conn, name, email, member_type):
    cur = conn.execute(
        "INSERT INTO members (name, email, type) VALUES (?, ?, ?)", (name, email, member_type)
    )
    return get(conn, cur.lastrowid)
