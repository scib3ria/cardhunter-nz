from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Card

DATABASE_URL = f"sqlite:///cardhunternz/db/card_data.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# Context manager wrapper
class SessionManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

# Shortcut for context-managed sessions
Session = lambda: SessionManager(SessionLocal)

def init_db():
    Base.metadata.create_all(bind=engine)
