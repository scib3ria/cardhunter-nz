from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    store = Column(String, index=True)
    game = Column(String, index=True)
    title = Column(String, index=True)
    variant_title = Column(String, nullable=True)
    price = Column(Float)
    quantity = Column(Integer)
    handle = Column(String, nullable=True)
    link = Column(String, nullable=True)
