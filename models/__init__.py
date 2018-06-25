from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .mark import Mark
from .cryptocurrency import Cryptocurrency
from .markCryptocurrency import Mark_Cryptocurrency
from .history import History
from .exchange import Exchange
from .orderBook import Orderbook
from .trade import Trade
from .symbol import Symbol
from .parameter import Parameter
from .base import Base

# engine = create_engine(os.environ['DATABASE_URL'])
engine = create_engine('sqlite:///crypto.db')

Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)