# database/user_manager.py

""" MANAGES USER ACCOUNT: REGISTRATION, LOGIN, READING_USER_INFORMATION"""
import hashlib # TO GET A HASH FUNCTION 
import os
import sqlite3

from database.db import get_connection

class UserManager:
    @staticmethod # IT IS STATIC BECAUSE WE WILL USE IT BEFORE HAVING "USER"-OBJECT
    def hash_password(password: str, salt: bytes = None) -> bytes:
        if salt is None:
            salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + key   # store salt + hash together
        # hashlib the library that have the functions
        # pbkdf2 loop 100 000 (protocol)
        # hmac mix salt and password
        # sha256 the how hmac mix (logic gates)

    @staticmethod
    def verify_password(stored: bytes, provided_password: str) -> bool:
        salt = stored[:32]
        stored_key = stored[32:]
        new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
        return new_key == stored_key

    @staticmethod
    def register(username: str, password: str) -> bool:
        """Returns True if registration succeeded, False if username exists."""
        hashed = UserManager.hash_password(password)
        try:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hashed)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def login(username: str, password: str) -> int or None:
        """Returns user_id if credentials correct, else None."""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id, password_hash FROM users WHERE username = ?",
                (username,)
            ).fetchone()
            if row and UserManager.verify_password(row['password_hash'], password):
                return row['id']
        return None

    @staticmethod
    def get_user_info(user_id: int):
        with get_connection() as conn:
            return conn.execute(
                "SELECT id, username, created_at FROM users WHERE id = ?",
                (user_id,)
            ).fetchone()
    

    @staticmethod
    def update_username(user_id: int, new_username: str) -> bool:
        """Change username. Returns True if successful, False if username already exists."""
        try:
            with get_connection() as conn:
                conn.execute(
                    "UPDATE users SET username = ? WHERE id = ?",
                    (new_username, user_id)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:  # username must be unique
            return False
    
    @staticmethod
    def change_password(user_id: int, old_password: str, new_password: str) -> bool:
        """
        Change user's password.
        Returns True if successful (old password matched).
        Returns False if old password is incorrect.
        """
        # First, verify the old password
        with get_connection() as conn:
            row = conn.execute(
                "SELECT password_hash FROM users WHERE id = ?",
                (user_id,)
            ).fetchone()
            if not row:
                return False
            if not UserManager.verify_password(row['password_hash'], old_password):
                return False
        
        # Hash the new password
        new_hash = UserManager.hash_password(new_password)
        
        # Update the database
        with get_connection() as conn:
            conn.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (new_hash, user_id)
            )
            conn.commit()
        return True
