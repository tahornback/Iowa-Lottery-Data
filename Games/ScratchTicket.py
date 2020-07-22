from Games.Game import Game


class ScratchTicket(Game):
    def __init__(self, id, db, price=-1):
        # Must be passed a price in order to guarantee proper calculations, as not all lowest prizes are always the cost
        self.type = Game.SCRATCH_TICKET_STRING
        self.link = (
            db.getSingleUrl(self.type)
            + str(id)
        )
        super().__init__(id, db, price)
