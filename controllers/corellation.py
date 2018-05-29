import models
import numpy as np

session = models.Session()

class History(object):
    def getHistory(self, session):
        session.query(models.History).get({"x": 5})

def animate(i, a):
    # 1. get data
    # 2  standart
    #history = session.query(models.History).all()
    #filter only usd, but over the ids
    history = session.query(models.History).filter(quote_currency = 'USD')
    currencies = session.query(models.Cryptocurrency).all

    historyarr = np.array(history)

    output = {}
    currencies_indexed = {}
    #indexBy
    for curr in currencies:
        currencies_indexed[curr.id] = curr
        output[curr.id] = []
    # 3. loop
    for i in history:
        output[i.quote_currecncy].push(i)

    #diff curr have diff time???
    session.commit()
    return True