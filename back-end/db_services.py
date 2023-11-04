import os
from sys import stderr, exit
import sqlite3

DB_PATH = os.path.dirname(__file__)+'/database.sqlite'


def top_n_players(n=10)->list[tuple]:
    connection, cursor = connect_db()
    params = {
        'num' : n,
    }
    query = '''
    SELECT player_id, score
    FROM scores
    ORDER BY score DESC
    LIMIT :num;
    '''
    cursor.execute(query, params)
    result = cursor.fetchall()
    close_connection(connection, cursor)
    return result
    
def add_player(id):
    connection, cursor = connect_db()
    query = '''
    INSERT INTO scores (player_id, score)
    VALUES (?, ?);
    '''
    cursor.execute(query, id, 0)
    close_connection(connection, cursor)

def update_score(id):
    connection, cursor = connect_db()
    query = '''
    UPDATE scores
    SET score = score + 1
    WHERE player_id = ?;
    '''
    cursor.execute(query, id)
    close_connection(connection, cursor)

def connect_db() -> (sqlite3.Connection, sqlite3.Cursor):
    """connect to sqlite database
        return connection and cursor
    """
    try:
        if os.path.exists(DB_PATH):
            connection = sqlite3.connect(DB_PATH, isolation_level=None, uri=True)
            cursor = connection.cursor()
            return connection, cursor
        else:
            print(f"Database file at {DB_PATH} does not exist.")
            exit(-1)
    except sqlite3.Error as e:
        print(e, file=stderr)
        exit(1)


def close_connection(connection: sqlite3.Connection, cursor: sqlite3.Cursor):
    """close the database connection
    """
    try:
        cursor.close()
        connection.close()
    except sqlite3.Error as e:
        print(e, file=stderr)