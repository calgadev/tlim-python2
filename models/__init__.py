# All models must be imported here so SQLAlchemy registers them with Base
# before Base.metadata.create_all() is called in main.py.
#
# Import order follows dependency hierarchy:
# User and Server have no dependencies, so they come first.
# Character depends on both User and Server, so it comes last.
from models.user import User
from models.server import Server
from models.character import Character