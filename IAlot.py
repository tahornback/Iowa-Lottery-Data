from Games.AllInstaPlays import AllInstaPlays
from Games.AllPullTabs import AllPullTabs
from Games.AllScratchTickets import AllScratchTickets
from database import GameDatabase

if __name__ == "__main__":
    db = GameDatabase()
    db.initTables()
    st = AllScratchTickets(db)
    ip = AllInstaPlays(db)
    pt = AllPullTabs(db)
    st.printAllScratchTickets()
    ip.printAllInstaPlays()
    pt.printAllPullTabs()
