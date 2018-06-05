import models
import numpy as np

session = models.Session()


class History(object):

    def getHistory(self, session):
        session.query(models.History).get({"x": 5})

    def get_correlation(self):
        session = models.Session()
        symbol_global_id = 'BITSTAMP_SPOT_BTC_USD'
        symbols = session.query(models.Symbol).filter(models.Symbol.symbol_global_id == symbol_global_id).all()
        if len(symbols) > 0:
            symbol_id = symbols[0].id
            result = session.query(models.History).filter(models.History.symbol_id == symbol_id).all()
            return result

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

tar = History()
test = tar.get_correlation()
