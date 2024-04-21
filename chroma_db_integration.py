import sqlite3

DATABASE_FILE = "C:\Data\Adrian\Github\GDSC-Hackathon\chroma.sqlite3"

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    return conn

def create_table_queries(conn):
    """Create the 'queries' table in the database."""
    sql = """
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY,
        query TEXT,
        response TEXT,
        format INTEGER
    );
    """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def insert_query_response(conn, query, response, format_step):
    """Insert a new query, response, and format into the 'queries' table."""
    sql = ''' INSERT INTO queries(query, response, format) VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (query, response, format_step))
    conn.commit()
    return cur.lastrowid

def main():
    conn = create_connection()
    create_table_queries(conn)
    conn.close()

if __name__ == "__main__":
    main()
