from Games.Game import Game


class InstaPlay(Game):
    def __init__(self, id, db, price=-1):
        # Must be passed a price in order to guarantee proper calculations, as not all lowest prizes are always the cost
        self.type = Game.INSTA_PLAY_STRING
        self.link = (
            "https://ialottery.com/Pages/Games-InstaPlay/InstaPlayGamesDetail.aspx?g="
            + str(id)
        )
        super().__init__(id, db, price)

        # Value of jackpot to make progressive jackpot instaplay "worthwhile", i.e. onDollar > 1
        self.worthwhileValue = self.calculateWorthwhileValue()

    def calculateWorthwhileValue(self):
        fakeOnDollar = 0
        necessaryJackpot = self.prizeMoney[-1]
        while fakeOnDollar < 1:
            fakeRoi = super().calculateROI(necessaryJackpot)
            fakeOnDollar = fakeRoi / self.price
            necessaryJackpot += 1
        return necessaryJackpot
