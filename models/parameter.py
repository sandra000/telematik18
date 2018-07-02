from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from .base import Base


class Parameter(Base):
    __tablename__ = 'parameters'

    id = Column(Integer, primary_key=True)
    period_id = Column(String(250), nullable=False)
    time_start = Column(String(250), nullable=False)
    time_end = Column(String(250), nullable=True)
    limit = Column(String(250), nullable=True)

    #def __init__(self, name):
    #    self.name = name

    def __repr__(self):
        return '<Parameter: {}>'.format(self.id)