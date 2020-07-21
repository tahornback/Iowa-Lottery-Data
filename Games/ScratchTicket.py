from Games.Game import Game


class ScratchTicket(Game):
    def __init__(self, id, price=-1):
        # Must be passed a price in order to guarantee proper calculations, as not all lowest prizes are always the cost
        self.type = Game.SCRATCHTICKETSTRING
        self.link = (
                "https://ialottery.com/Pages/Games-Scratch/ScratchGamesDetail.aspx?g="
                + str(id)
        )
        super().__init__(id, price)
