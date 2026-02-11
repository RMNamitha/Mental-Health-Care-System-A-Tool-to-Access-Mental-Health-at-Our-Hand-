import sqlite3
from datetime import datetime, timedelta

# Connect to database
conn = sqlite3.connect("mindcare.db", check_same_thread=False)
cur = conn.cursor()



# Create tables
def create_tables():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            username TEXT,
            phq INTEGER,
            gad INTEGER,
            date TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            username TEXT,
            message TEXT,
            emotion TEXT,
            date TEXT
        )
    """)
    conn.commit()

# User management
def add_user(username, password):
    try:
        cur.execute("INSERT INTO users VALUES (?,?)", (username, password))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cur.fetchone()

# Scores
def save_score(username, phq, gad):
    cur.execute(
        "INSERT INTO scores VALUES (?,?,?,?)",
        (username, phq, gad, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()

def get_scores(username):
    cur.execute("SELECT phq, gad, date FROM scores WHERE username=?", (username,))
    return cur.fetchall()

def get_latest_score(username):
    cur.execute("SELECT phq, gad, date FROM scores WHERE username=? ORDER BY date DESC LIMIT 1", (username,))
    return cur.fetchone()

# Chats
def save_chat(username, message, emotion):
    cur.execute(
        "INSERT INTO chats VALUES (?,?,?,?)",
        (username, message, emotion, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()

def get_chat_history(username):
    cur.execute("SELECT message, emotion, date FROM chats WHERE username=?", (username,))
    return cur.fetchall()

# Weekly report
def get_weekly_report(username):
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    cur.execute(
        "SELECT phq, gad, date FROM scores WHERE username=? AND date>=?", 
        (username, week_ago)
    )
    scores = cur.fetchall()
    
    cur.execute(
        "SELECT message, emotion, date FROM chats WHERE username=? AND date>=?",
        (username, week_ago)
    )
    chats = cur.fetchall()
    
    return scores, chats
