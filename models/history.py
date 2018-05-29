from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base
from .cryptocurrency import Cryptocurrency
from .mark import Mark


class History(Base):
    __tablename__ = 'histories'

    id = Column(Integer, primary_key=True)
    start_time_exchange = Column(DateTime)
    last_time_exchange = Column(DateTime)
    ask_price = Column(Float)
    ask_size = Column(Float)
    last_ask_price = Column(Float)
    last_ask_size = Column(Float)
    base_currency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    quote_currency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    mark_id = Column(Integer, ForeignKey('marks.id'), nullable=True)

    base_currency = relationship(Cryptocurrency, primaryjoin=base_currency_id == Cryptocurrency.id)
    quote_currency = relationship(Cryptocurrency, primaryjoin=quote_currency_id == Cryptocurrency.id)
    #mark = relationship(Mark)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<History: {}>'.format(self.id)