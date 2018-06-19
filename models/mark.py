from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .markCryptocurrency import Mark_Cryptocurrency
from .base import Base


# it is only for Market/Exchange API

class Mark(Base):

    __tablename__ = 'marks'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    api_url = Column(String(250), nullable=False)
    website = Column(String(250), nullable=True)
    exchange_global_id = Column(String(250), nullable=True)
    histories = relationship("History", backref="mark")
    currency = relationship('Mark_Cryptocurrency', backref='mark', primaryjoin=id == Mark_Cryptocurrency.mark_id)

    # for now this relation many to many not used

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Mark: {}>'.format(self.id)