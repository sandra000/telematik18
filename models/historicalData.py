from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from .base import Base


class Mark(Base):
    __tablename__ = 'marks'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    api_url = Column(String(250), nullable=False)
    histories = relationship("History", backref="mark")


class History(Base):
    __tablename__ = 'histories'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    start_time_exchange = Column(DateTime)
    last_time_exchange = Column(DateTime)
    ask_price = Column(Float)
    ask_size = Column(Float)
    last_ask_price = Column(Float)
    last_ask_size = Column(Float)
    mark_id = Column(Integer, ForeignKey('marks.id'))
    mark = relationship(Mark, primaryjoin=mark_id == Mark.id)