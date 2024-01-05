import sqlite3


def create_connection(db):

    conn = None
    try:
        conn = sqlite3.connect(db)
    except Exception as e:
        print(e)

    return conn
