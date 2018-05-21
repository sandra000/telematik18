from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import base

#engine = create_engine(os.environ['DATABASE_URL'])
engine = create_engine('sqlite:///crypto.db')

Session = sessionmaker(bind=engine)
base.Base.metadata.create_all(engine)