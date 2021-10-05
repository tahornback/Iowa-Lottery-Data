import urllib.request

from bs4 import *


class Game:
    INVALID_GAME = "Invalid Game"
    SCRATCH_TICKET_STRING = "scratch"
    INSTA_PLAY_STRING = "instaplay"
    PULL_TAB_STRING = "pulltab"

    def __init__(self, id, db, price=-1):
        self.id = id
        self.price = price
        self.gameName = self.INVALID_GAME
        self.validGame = False
        self.odds = None
        self.overallOdds = None
        self.roi = None
        self.onDollar = None
        self.prizeMoney = None
        self.database = db  # Preferably this would be from dependency injection

        query = self.database.getGame(self)
        if query is not None:
            print(self.id, "found in db")
            # print(query)
            self.validGame = True
            self.gameName = query[2]
            self.prizeMoney = self.stringListToFloatList(self.stringToList(query[3]))
            self.odds = self.stringListToFloatList(self.stringToList(query[4]))
        else:
            print(self.id, "not found in db")
            try:
                site = urllib.request.urlopen(self.link)
                soup = BeautifulSoup(site, features="html.parser")
                self.parseValuesFromSoup(soup)
                self.calculateNonSoupValues()
                db.addGame(self)
            except AttributeError as err:
                print(err)
                self.invalidAll()
        self.calculateNonSoupValues()
        self.attrs = {
            "validGame": self.validGame,
            "gameName": self.gameName,
            "odds": self.odds,
            "prizeMoney": self.prizeMoney,
            "overallOdds": self.overallOdds,
            "roi": self.roi,
            "onDollar": self.onDollar,
        }



    def invalidAll(self):
        self.gameName = self.INVALID_GAME
        self.validGame = False
        self.odds = None
        self.overallOdds = None
        self.roi = None
        self.onDollar = None
        self.prizeMoney = None

    def calculateNonSoupValues(self):
        self.calculateOverallOdds()
        self.CalculateROI()

    def CalculateROI(self):
        self.roi = 0
        self.price = self.prizeMoney[0] if self.price == -1 else self.price
        for pos in range(len(self.odds)):
            self.roi += self.prizeMoney[pos] / self.odds[pos]
        self.onDollar = self.roi / self.price

    def calculateOverallOdds(self):
        self.overallOdds = 0
        for odd in self.odds:
            self.overallOdds += 1 / odd

    def parseValuesFromSoup(self, soup):
        self.gameName = soup.find(
            id="ContentPlaceHolder1_gameDetail_GameName"
        ).text
        prizeSet = soup.find(id="Prizes")
        self.validGame = True
        table = prizeSet.find_all("td")
        self.prizeMoney = []
        self.odds = []
        for row in range(0, len(table) - 2, 2):
            temp = table[row].text[1:]
            if temp == "ackpot*":
                temp = soup.find(id="ContentPlaceHolder1_lblIPJPAmount").text[
                       1:
                       ]
            if temp[0] == "$":
                temp = temp[1:]
            temp = temp.replace(",", "")
            temp = float(temp)
            self.prizeMoney.append(temp)
            split = table[row + 1].text.split(" ")
            self.odds.append(float(split[3].replace(",", "")))

    def sortByGameName(self):
        return self.attrs["gameName"]

    def sortByOverallOdds(self):
        return self.attrs["overallOdds"]

    def sortByRoi(self):
        return self.attrs["roi"]

    def sortByOnDollar(self):
        return self.attrs["onDollar"]

    def calculateROI(self, jackpot=0):
        # Returns new ROI if jackpot is nonzero or prizeMoney/odds have been modified.
        roi = 0
        for pos in range(len(self.odds) - 1):
            roi += self.prizeMoney[pos] * self.odds[pos]
        if jackpot != 0:
            roi += jackpot * self.odds[-1]
        else:
            roi += self.prizeMoney[-1] * self.odds[-1]
        return roi

    def __str__(self):
        toReturn = ""
        if self.validGame:
            toReturn += (
                    "Name/ID: "
                    + self.gameName
                    + "/"
                    + str(self.id)
                    + "\nPrice ${0:.2f}".format(self.price)
                    + "\nOdds: {0:.1%}".format(self.overallOdds)
                    + "\nExpected ROI: ${0:.2f}".format(self.roi)
                    + "\nCents on the dollar: ¢{0:.1f}".format(100 * self.onDollar)
            )
            if self.type == self.INSTA_PLAY_STRING:
                toReturn += "\nWorthwhile Jackpot Value: ${:,}".format(
                    self.worthwhileValue
                )
        else:
            return self.INVALID_GAME
        return toReturn

    def stringToList(self, string):
        return string.replace("[","").replace("]","").split(", ")

    def stringListToFloatList(self, inList):
        outList = []
        for elem in inList:
            outList.append(float(elem))
        return outList