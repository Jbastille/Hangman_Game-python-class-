""" THIS FILE MANAGE CONNECTION TO SQLite & CREATE TABLES"""


import sqlite3 # BUILD-IN LIBRARY FOR SQLite
import os   # TO CREATE FILE PATHS THAT WORK IN ANY OPERATING SYSTEM

DB_PATH = os.path.join(os.path.dirname(__file__), 'hangman.db') # THE PATH WHERE THE DATABASE WILL BE CREATED

def get_connection():
    """give access by memory address that the SQLite database begins ."""
    # 
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # it a setting that , it converts the rows that it by defaults is tuples into Row objects  so we can access them by name
    return conn

def init_db():
    """Create tables if they don't exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Scores table – each game result linked to a user
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                word TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                attempts_used INTEGER NOT NULL,
                hints_used INTEGER DEFAULT 0,
                time_seconds INTEGER,          -- 
                won BOOLEAN NOT NULL,
                score INTEGER,                
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        # leaderboard view 
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scores_user ON scores(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scores_difficulty ON scores(difficulty)')
        conn.commit()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                theme TEXT,
                difficulty TEXT NOT NULL,
                usage_count INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_words_difficulty ON words(difficulty)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_words_category ON words(category)')

# Initialize DB every time  this module is imported
init_db()