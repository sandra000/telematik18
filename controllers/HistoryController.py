import models
import numpy as np
import pandas as pd


class History(object):

    session = models.Session()

    def get_history_by_base_currency(self, currency_id):
        return self.session.query(models.History).join(models.History.base_currency).filter(models.History.base_currency_id == currency_id).all()

    def get_all_history(self):
        #return self.session.query(models.History).join(models.History.base_currency).all()
        query = self.session.query(models.History).join(models.History.base_currency)
        return pd.read_sql(query.statement, self.session.bind)

    def get_all_base_currency_from_history(self):
        return self.session.query(models.History).group_by(models.History.base_currency_id).all()


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
