from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# The database will be a file called tlim.db in the project root.
# SQLite requires no installation — it's just a file on disk.
SQLALCHEMY_DATABASE_URL = "sqlite:///./tlim.db"

# The engine manages the connection to the database.
# check_same_thread=False is required for SQLite to work with FastAPI,
# which may use different threads to handle requests.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal is the session factory.
# Each request will open a session, use it, and close it when done.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the class that all models will inherit from.
# SQLAlchemy uses it to keep track of which tables exist.
class Base(DeclarativeBase):
    pass

# This function is used in routers to open and close the database session
# safely — even if an error occurs, the finally block ensures it closes.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()