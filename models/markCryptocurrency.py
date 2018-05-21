from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from .base import Base


class Mark_Cryptocurrency(Base):
    __tablename__ = 'mark_cryptocurrency'

    id = Column(Integer, primary_key=True)
    mark_id = Column(Integer, ForeignKey('marks.id'), primary_key=True)
    cryptocurrency_id = Column(Integer, ForeignKey('cryptocurrencies.id'), primary_key=True)

    mark = relationship("Mark", backref=backref("mark_cryptocurrency", cascade="all, delete-orphan"))
    cryptocurrency = relationship("Cryptocurrency", backref=backref("mark_cryptocurrency",
                                                                    cascade="all, delete-orphan"))

    def __init__(self, name):
        self.name = name
