import os
import sqlite3
from sqlite3 import Error


class GameDatabase:
    def __init__(self):
        self.DB_PATH = os.getcwd() + "\\db.sqlite"
        self.connection = None
        self.cursor = None
        try:
            self.connection = sqlite3.connect(self.DB_PATH)
            print("Connection to SQLite DB successful")
            self.cursor = self.connection.cursor()
            print("Cursor successfully created")
        except Error as e:
            print(f"The error '{e}' occurred")

    def isAlive(self):
        return self.connection is not None and self.cursor is not None

    def initTables(self):
        if self.isAlive():
            try:
                self.cursor.execute(
                    "CREATE TABLE Game (Id real, Type text, Name text, Prizes text, Odds text)"
                )
                print("Successfully initialized tables")
            except Error as e:
                print(f"The error '{e}' occurred")

    def findGameById(self, gameId):
        print(gameId)
        if self.isAlive():
            return self.cursor.execute("SELECT * FROM Game WHERE Id=?", (gameId,)).fetchall()
