import sqlite3
import os

def create_db():
    if not os.path.exists("users_blackdjack.db"):
        conn = sqlite3.connect('users_blackdjack.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE users
                    (user_id integer, first_name text, balance integer, kd real, count_games integer, wins integer)''')

        conn.commit()
        conn.close()

def add_user(user_id, first_name):
    conn = sqlite3.connect('users_blackdjack.db')
    c = conn.cursor()

    c.execute("INSERT INTO users (user_id, first_name, balance, kd, count_games, wins) VALUES (?,?,?,?,?,?)", (user_id, first_name, 0, 1.0, 0, 0))

    conn.commit()
    conn.close()

def update_user(user_id, first_name, balance, kd, count_games, wins):
    conn = sqlite3.connect('users_blackdjack.db')
    c = conn.cursor()

    c.execute("UPDATE users SET first_name = ?, balance = ?, kd = ?, count_games = ?, wins = ? WHERE user_id = ?", (first_name, balance, kd, count_games, wins, user_id))

    conn.commit()
    conn.close()

def get_user_info(user_id):
    conn = sqlite3.connect('users_blackdjack.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()

    conn.close()
    return user

def delete_user(user_id):
    conn = sqlite3.connect('users_blackdjack.db')
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

def add_or_update_user(user_id, first_name, balance, kd, count_games, wins):
    conn = sqlite3.connect('users_blackdjack.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()

    if user:
        pass
    else:
        c.execute("INSERT INTO users (user_id, first_name, balance, kd, count_games, wins) VALUES (?,?,?,?,?,?)", (user_id, first_name, balance, kd, count_games, wins))

    conn.commit()
    conn.close()

def increment_count_games(user_id):
    conn = sqlite3.connect('users_blackdjack.db')
    c = conn.cursor()

    c.execute("UPDATE users SET count_games = count_games + 1 WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

def get_top_players():
    conn = sqlite3.connect('users_blackdjack.db')
    c = conn.cursor()

    c.execute("SELECT first_name, count_games, kd FROM users ORDER BY count_games DESC LIMIT 10")
    top_players = c.fetchall()

    conn.close()
    return top_players
