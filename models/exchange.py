from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base
from .cryptocurrency import Cryptocurrency
from .mark import Mark


class Exchange(Base):
    __tablename__ = 'exchanges'

    id = Column(Integer, primary_key=True)
    time_exchange = Column(DateTime)
    rate = Column(Float)
    base_currency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    quote_currency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    mark_id = Column(Integer, ForeignKey('marks.id'))

    base_currency = relationship(Cryptocurrency, primaryjoin=base_currency_id == Cryptocurrency.id)
    quote_currency = relationship(Cryptocurrency, primaryjoin=quote_currency_id == Cryptocurrency.id)
    mark = relationship(Mark, primaryjoin=mark_id == Mark.id)

    def __init__(self, name):
        self.name = name
