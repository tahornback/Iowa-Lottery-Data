from Games.AllInstaPlays import AllInstaPlays
from Games.AllPullTabs import AllPullTabs
from Games.AllScratchTickets import AllScratchTickets
from database import GameDatabase
import ssl

if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    db = GameDatabase()
    # db.dumpContents()
    st = AllScratchTickets(db)
    ip = AllInstaPlays(db)
    # pt = AllPullTabs(db)
    st.printAllScratchTickets()
    ip.printAllInstaPlays()
    # pt.printAllPullTabs()
    # db.dumpContents()
