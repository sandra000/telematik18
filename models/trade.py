from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, Boolean
from sqlalchemy.orm import relationship
from .cryptocurrency import Cryptocurrency
from .mark import Mark
from .base import Base


#TODO: Maybe have only one table for orderbook and for trade
class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    price = Column(Float)
    size = Column(Float)
    type = Column(Boolean) # asks or bids, true === ask false == bids
    base_currency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    quote_currency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    mark_id = Column(Integer, ForeignKey('marks.id'))

    base_currency = relationship(Cryptocurrency, primaryjoin=base_currency_id == Cryptocurrency.id)
    quote_currency = relationship(Cryptocurrency, primaryjoin=quote_currency_id == Cryptocurrency.id)
    mark = relationship(Mark, primaryjoin=mark_id == Mark.id)

    def __init__(self, name):
        self.name = name
