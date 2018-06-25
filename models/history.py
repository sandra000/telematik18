from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base
from .cryptocurrency import Cryptocurrency
from .parameter import Parameter
from .mark import Mark
from .symbol import Symbol

#OHLCV
class History(Base):
    __tablename__ = 'histories'

    id = Column(Integer, primary_key=True)
    start_time_exchange = Column(DateTime)
    last_time_exchange = Column(DateTime)
    ask_price = Column(Float)#open
    ask_size = Column(Float)
    ask_price_last = Column(Float)
    ask_size_last = Column(Float)# do we need this?
    ask_price_high = Column(Float)# open
    ask_price_low = Column(Float)
    base_currency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    quote_currency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    symbol_id = Column(Integer, ForeignKey('symbols.id'), nullable=True)
    mark_id = Column(Integer, ForeignKey('marks.id'), nullable=True)# this if we want to use something else as coinapi
    parameter_id = Column(Integer, ForeignKey('parameters.id'), nullable=True)

    base_currency = relationship(Cryptocurrency, primaryjoin=base_currency_id == Cryptocurrency.id)
    quote_currency = relationship(Cryptocurrency, primaryjoin=quote_currency_id == Cryptocurrency.id)
    parameter = relationship(Parameter, primaryjoin=parameter_id == Parameter.id)
    #symbol = relationship(Symbol, primaryjoin=symbol_id == Symbol.id)
    #mark = relationship(Mark)

    def __repr__(self):
        return '<History: {}>'.format(self.id)