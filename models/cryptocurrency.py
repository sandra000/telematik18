from sqlalchemy import Column, Integer, String
from .markCryptocurrency import Mark_Cryptocurrency
from sqlalchemy.orm import relationship
from .base import Base


class Cryptocurrency(Base):
    __tablename__ = 'cryptocurrencies'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    name_id = Column(String(250), nullable=False)
    mark = relationship('Mark_Cryptocurrency', backref='cryptocurrency',
                        primaryjoin=id == Mark_Cryptocurrency.cryptocurrency_id)

    def __init__(self, name):
        self.name = name
