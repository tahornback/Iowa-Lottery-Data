import os
import sqlite3
from sqlite3 import Error
from Games.Game import Game
import atexit


class GameDatabase:
    def __init__(self):
        # try:
        #     os.remove("db.sqlite")
        # except FileNotFoundError:
        #     pass
        self.DB_PATH = os.getcwd() + "\\db.sqlite"
        self.connection = None
        self.cursor = None
        try:
            self.connection = sqlite3.connect(self.DB_PATH)
            print("Connection to SQLite DB successful")
            self.cursor = self.connection.cursor()
            print("Cursor successfully created")
            if not self.cursor.execute("SELECT * FROM sqlite_master").fetchone():
                self.initTables()
                print("Tables initialized")
            else:
                print("Tables already initialized")
            atexit.register(self.exit)
        except Error as e:
            print(f"The error '{e}' occurred when initializing database")

    def isAlive(self):
        return self.connection is not None and self.cursor is not None

    # Make this into actual migrations instead of this jank
    def initTables(self):
        if self.isAlive():
            gameTypeToExecute = [
                "CREATE TABLE GameType (Id INTEGER PRIMARY KEY, Type text, Name text, SingleUrl text, AllUrl text)",
                "INSERT INTO GameType (Type, Name, SingleUrl, AllUrl) VALUES ('{}', 'Scratch', "
                "'https://ialottery.com/Pages/Games-Scratch/ScratchGamesDetail.aspx?g=', "
                "'https://ialottery.com/Pages/Games-Scratch/ScratchGamesListing.aspx')".format(
                    Game.SCRATCH_TICKET_STRING
                ),
                "INSERT INTO GameType (Type, Name, SingleUrl, AllUrl) VALUES ('{}', 'InstaPlay', "
                "'https://ialottery.com/Pages/Games-InstaPlay/InstaPlayGamesDetail.aspx?g=', "
                "'https://ialottery.com/Pages/Games-InstaPlay/InstaPlay.aspx')".format(
                    Game.INSTA_PLAY_STRING
                ),
                "INSERT INTO GameType (Type, Name, SingleUrl, AllUrl) VALUES ('{}', 'Pulltab', "
                "'https://ialottery.com/Pages/Games-Pulltab/PulltabGamesDetail.aspx?g=', "
                "'https://ialottery.com/Pages/Games-Pulltab/PulltabGamesListing.aspx')".format(
                    Game.PULL_TAB_STRING
                ), "CREATE TABLE Game (Id INTEGER PRIMARY KEY, Type real, Name text, Prizes text, Odds text, "
                             "FOREIGN KEY (Type) REFERENCES GameType (Id)) ",
            ]

            for q in gameTypeToExecute:
                try:
                    print(q)
                    self.cursor.execute(q)
                except Error as e:
                    print(f"The error '{e}' occurred when building tables")

    def getGame(self, game):
        if self.isAlive():
            gameTypeId = self.cursor.execute(
                "SELECT Type FROM GameType WHERE Type=?", (game.type,)
            ).fetchone()[0]
            return self.cursor.execute(
                "SELECT * FROM Game WHERE Id=? AND Type=?", (game.id, gameTypeId)
            ).fetchone()

    def addGame(self, game):
        print("adding {} to db".format(game.id))
        if self.isAlive():
            self.cursor.execute(
                "INSERT INTO Game (Id, Type, Name, Prizes, Odds) VALUES (?,?,?,?,?)",
                (game.id, game.type, game.gameName, str(game.prizeMoney), str(game.odds),),
            )

    def getSingleUrl(self, gameType):
        if self.isAlive():
            return self.cursor.execute(
                "SELECT SingleUrl FROM GameType WHERE Type=?", (gameType,)
            ).fetchone()[0]

    def getAllUrl(self, gameType):
        if self.isAlive():
            return self.cursor.execute(
                "SELECT AllUrl FROM GameType WHERE Type=?", (gameType,)
            ).fetchone()[0]

    def dumpContents(self):
        if self.isAlive():
            for table in self.cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall():
                contents = self.cursor.execute("SELECT * FROM " + table[0]).fetchall()
                for tup in contents:
                    print(*tup)

    def exit(self):
        print("closing cursor")
        self.cursor.close()
        print("cursor closed")
        print("committing db")
        self.connection.commit()
        print("committed to db")
