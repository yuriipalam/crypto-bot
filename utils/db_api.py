import sqlite3

from aiogram import types


class Database:
    def __init__(self, path="main.db"):
        self.path = path

    @property
    def _connection(self):
        return sqlite3.connect(self.path)

    def _execute(self, sql, parameters: tuple = tuple(), fetchone=False, fetchall=True, commit=False):
        connection = self._connection
        cursor = connection.cursor()
        cursor.execute(sql, parameters)

        data = None

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()

        return data

    def create_table_users(self):
        sql = """CREATE TABLE users(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER NOT NULL UNIQUE)"""
        self._execute(sql, commit=True)

    def add_user(self, user_id: int):
        sql = "INSERT INTO users (user_id) VALUES (?)"
        parameters = (user_id,)
        try:
            self._execute(sql=sql, parameters=parameters, commit=True)
        except sqlite3.IntegrityError:
            return None

    def select_all_users(self):
        sql = "SELECT user_id FROM users"
        return self._execute(sql, fetchall=True)