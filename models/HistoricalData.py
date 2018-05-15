import os
import sys
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Mark(Base):
    __tablename__ = 'mark'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    api_url = Column(String(250), nullable=False)


class History(Base):
    __tablename__ = 'history'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    start_time_exchange = Column(DateTime)
    last_time_exchange = Column(DateTime)
    ask_price = Column(Float)
    ask_size = Column(Float)
    last_ask_price = Column(Float)
    last_ask_size = Column(Float)
    person = relationship(Mark)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///crypto.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)