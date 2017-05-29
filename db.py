from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from settings import DB_URI

Session = sessionmaker(autocommit=True,
                       autoflush=True,
                       bind=create_engine(DB_URI, echo=False))
nonflask_session = scoped_session(Session)
