import urllib.request

from bs4 import *

from Games.Game import Game
from Games.InstaPlay import InstaPlay


class AllInstaPlays:
    def __init__(self, db):
        print("Initializing AllInstaPlays")
        self.type = Game.INSTA_PLAY_STRING
        site = urllib.request.urlopen(
            db.getAllUrl(self.type)
        )
        soup = BeautifulSoup(site, features="html.parser")
        scratchListTag = soup.find(id="scratchList")

        items = scratchListTag.find_all(href=True)
        self.games = []
        for item in items:
            price = item.find_all("span")[1].find_all("span")[0].text
            if price[0] == "$":
                price = float(price[1:])
            elif price[2] == "¢":
                price = float("0." + price[:2])
            self.games.append(InstaPlay(item["href"].split("=")[1], db, price))

    def __str__(self):
        toReturn = "Games:\n"
        for game in self.games:
            toReturn += game.gameName + "\n"
        return toReturn

    def printAllInstaPlays(self):
        print("InstaPlay Games")
        sortbygame = sorted(self.games, key=Game.sortByGameName)
        sortbyoverallodds = sorted(
            self.games, key=Game.sortByOverallOdds, reverse=True
        )
        sortbyondollar = sorted(
            self.games, key=Game.sortByOnDollar, reverse=True
        )
        print("\nsorted by name")
        for y in sortbygame:
            print(y, "\n")
        print("\nsorted by overall odds")
        for y in sortbyoverallodds:
            print(y, "\n")
        print("\nsorted by onDollar")
        for y in sortbyondollar:
            print(y, "\n")
