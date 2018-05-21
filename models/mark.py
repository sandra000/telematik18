from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from .markCryptocurrency import Mark_Cryptocurrency
from .base import Base


class Mark(Base):
    __tablename__ = 'marks'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    api_url = Column(String(250), nullable=False)
    website = Column(String(250), nullable=True)
    histories = relationship("History", backref="mark")
    currency = relationship('Mark_Cryptocurrency', backref='mark',
                         primaryjoin=id == Mark_Cryptocurrency.mark_id)

    def __init__(self, name):
        self.name = name
