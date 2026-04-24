import mysql.connector

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   # change if needed
            database="link_checker_db"
        )

        print("Connected to MySQL successfully")
        return conn

    except Exception as e:
        print("Error connecting to MySQL:", e)
        exit()


def create_tables(cursor):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS valid_links (
        id INT AUTO_INCREMENT PRIMARY KEY,
        url TEXT,
        status TEXT,
        time FLOAT,
        final_url TEXT,
        domain TEXT,
        checked_on TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS failed_links (
        id INT AUTO_INCREMENT PRIMARY KEY,
        url TEXT,
        status TEXT,
        time FLOAT,
        final_url TEXT,
        domain TEXT,
        checked_on TEXT
    )
    """)