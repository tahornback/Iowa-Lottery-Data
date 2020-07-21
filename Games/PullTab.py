from Games.Game import Game


class PullTab(Game):
    def __init__(self, id, price=-1):
        # Must be passed a price in order to guarantee proper calculations, as not all lowest prizes are the cost
        self.type = Game.PULLTABSTRING
        self.link = (
                "https://ialottery.com/Pages/Games-Pulltab/PulltabGamesDetail.aspx?g="
                + str(id)
        )
        super().__init__(id, price)
