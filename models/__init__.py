from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .historicalData import Base
from .exchangeRate import Base
from .orderBook import Base
from .trade import Base
from .base import Base

#engine = create_engine(os.environ['DATABASE_URL'])
engine = create_engine('sqlite:///crypto.db')

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)