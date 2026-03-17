# All models must be imported here so SQLAlchemy registers them with Base
# before Base.metadata.create_all() is called in main.py.
#
# Import order follows dependency hierarchy:
# User and Server have no dependencies, so they come first.
# Character depends on both User and Server, so it comes last.
from models.user import User
from models.server import Server
from models.item import Item
from models.creature import Creature
from models.character import Character
from models.server_item_price import ServerItemPrice
from models.inventory import Inventory
from models.hunt_session import HuntSession
from models.hunt_session_item import HuntSessionItem
from models.hunt_session_monster import HuntSessionMonster