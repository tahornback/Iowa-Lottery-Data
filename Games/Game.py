import urllib.request

from bs4 import *


class Game:
    INVALIDGAME = "Invalid Game"
    SCRATCHTICKETSTRING = "scratch"
    INSTAPLAYSTRING = "instaplay"
    PULLTABSTRING = "pulltab"

    def __init__(self, id, price=-1):
        self.id = id
        self.site = urllib.request.urlopen(self.link)
        self.soup = BeautifulSoup(self.site, features="html.parser")
        try:
            self.gameName = self.soup.find(
                id="ContentPlaceHolder1_gameDetail_GameName"
            ).text
            prizeSet = self.soup.find(id="Prizes")
            self.validGame = True
            table = prizeSet.find_all("td")
            self.prizeMoney = []
            self.odds = []
            for row in range(0, len(table) - 2, 2):
                temp = table[row].text[1:]
                if temp == "ackpot*":
                    temp = self.soup.find(id="ContentPlaceHolder1_lblIPJPAmount").text[
                        1:
                    ]
                if temp[0] == "$":
                    temp = temp[1:]
                temp = temp.replace(",", "")
                temp = float(temp)
                # temp = int(temp)
                self.prizeMoney.append(temp)
                split = table[row + 1].text.split(" ")
                oddsDecimal = float(split[1].replace(",", "")) / float(
                    split[3].replace(",", "")
                )
                self.odds.append(oddsDecimal)
            self.overallOdds = 0
            for odd in self.odds:
                self.overallOdds += odd
            self.roi = 0
            if price == -1:
                self.price = self.prizeMoney[0]
            else:
                self.price = price
            for pos in range(len(self.odds)):
                self.roi += self.prizeMoney[pos] * self.odds[pos]
            self.onDollar = self.roi / self.price
        except AttributeError as err:
            print(err)
            self.gameName = self.INVALIDGAME
            self.validGame = False
            self.odds = None
            self.overallOdds = None
            self.roi = None
            self.onDollar = None
            self.prizeMoney = None
        self.attrs = {
            "validGame": self.validGame,
            "gameName": self.gameName,
            "odds": self.odds,
            "prizeMoney": self.prizeMoney,
            "overallOdds": self.overallOdds,
            "roi": self.roi,
            "onDollar": self.onDollar,
        }

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
            if self.type == self.INSTAPLAYSTRING:
                toReturn += "\nWorthwhile Jackpot Value: ${:,}".format(
                    self.worthwhileValue
                )
        else:
            return self.INVALIDGAME
        return toReturn
