import sqlite3
import hashlib

class UserManager:
    def __init__(self, db_name='user-password.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                name TEXT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        con.commit()
        con.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, name, username, password, confirm_password):
        if password != confirm_password:
            return "Passwords do not match."

        hashed = self.hash_password(password)

        try:
            con = sqlite3.connect(self.db_name)
            cursor = con.cursor()
            cursor.execute("INSERT INTO USERS (name, username, password) VALUES (?, ?, ?)",
                           (name, username, hashed))
            con.commit()
            return "User registered successfully."
        except sqlite3.IntegrityError:
            return "Username already exists."
        finally:
            con.close()

    def get_user(self, username):
        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()
        cursor.execute("SELECT name, username, password FROM USERS WHERE username = ?", (username,))
        user = cursor.fetchone()
        con.close()
        return user

    def login_user(self, username, password):
        user = self.get_user(username)
        if not user:
            return "User not found."
        if user[2] == self.hash_password(password):
            return f"Welcome, {user[0]}!"
        else:
            return "Incorrect password."

    def update_user(self, username, new_name=None, new_password=None, confirm_password=None):
        if new_password and confirm_password and new_password != confirm_password:
            return "Passwords do not match."

        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()

        updates = []
        values = []

        if new_name:
            updates.append("name = ?")
            values.append(new_name)
        if new_password:
            updates.append("password = ?")
            values.append(self.hash_password(new_password))

        if not updates:
            return "No updates provided."

        values.append(username)
        query = f"UPDATE USERS SET {', '.join(updates)} WHERE username = ?"

        cursor.execute(query, values)
        con.commit()
        con.close()
        return "User updated successfully."

    def list_users(self):
        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()
        cursor.execute("SELECT name, username FROM USERS")
        users = cursor.fetchall()
        con.close()
        return users
