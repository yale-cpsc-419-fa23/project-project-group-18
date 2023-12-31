import os
from sys import stderr, exit
import sqlite3

DB_PATH = os.path.dirname(__file__)+'/database.sqlite'

def user_login(username, password):
    connection, cursor = connect_db()
    params = {
        'username' : str(username),
    }
    query = '''
    SELECT password FROM users
    WHERE username = :username;
    '''
    cursor.execute(query, params)
    user = cursor.fetchone()
    print(user)
    close_connection(connection, cursor)
    if not user:
        print("Username not existed.")
        return False
    elif user[0] != password:
        print("Password not matched.")
        return False
    
    if user[0] == password:
        print("Successfully logined.")
        return True
    
    print("Failed to login.")
    return False


def user_register(username, password, email):
    connection, cursor = connect_db()
    params = {
        'username' : str(username),
        'password' : str(password),
        'email' : str(email),
    }
    query = '''
    SELECT * FROM users
    WHERE username = :username OR email = :email;
    '''
    cursor.execute(query, params)
    user = cursor.fetchone()
    if user:
        print("Username/email already existed.")
        is_success = False
    else:
        statement = "INSERT INTO users (username, password, email) VALUES (:username, :password, :email)"
        cursor.execute(statement, params)
        connection.commit()
        print("New user created.")
        is_success = True
    close_connection(connection, cursor)
    return is_success

def user_ranking(user_id):
    connection, cursor = connect_db()
    params = {
        'user_id' : str(user_id),
    }
    query = '''
    SELECT COALESCE(
       (SELECT rank FROM
        (SELECT
            player_id,
            RANK() OVER (ORDER BY score DESC) as rank
            FROM scores)
        WHERE player_id = :user_id),
        (SELECT COUNT(*) FROM scores)
    ) AS result;
    '''
    cursor.execute(query, params)
    user = cursor.fetchone()
    ranking = user[0]

    close_connection(connection, cursor)
    return ranking
    

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
    params = {
        'player_id' : id,
        'score': 0,
    }
    query = '''
    INSERT INTO scores (player_id, score)
    VALUES (:player_id, :score);
    '''
    cursor.execute(query, params)
    connection.commit()
    close_connection(connection, cursor)

def update_score(id):
    connection, cursor = connect_db()
    params = {
        'player_id' : id,
    }
    query = '''
    UPDATE scores
    SET score = score + 10
    WHERE player_id = :player_id;
    '''
    cursor.execute(query, params)
    connection.commit()
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


if __name__ == '__main__':
    #user_register('sauki3', '123456', 'sauki@yale.edu')
    #user_login('sauki3', '123456')
    x=  user_ranking('sauki')
    print(x)
