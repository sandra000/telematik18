from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from .base import Base


class Symbol(Base):
    __tablename__ = 'symbols'

    id = Column(Integer, primary_key=True)
    mark_id = Column(Integer, ForeignKey('marks.id'))
    symbol_global_id = Column(String(250), nullable=True)
    base_cryptocurrency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    quote_cryptocurrency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))

    mark = relationship("Mark", backref=backref("mark_cryptocurrency", cascade="all, delete-orphan"))
    #cryptocurrency = relationship("Cryptocurrency", backref=backref("mark_cryptocurrency", cascade="all, delete-orphan"))

    def __init__(self,mark_id):
        self.mark_id= mark_id

    def __repr__(self):
        return '<Symbol: {}>'.format(self.id)