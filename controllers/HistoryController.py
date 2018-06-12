import models
import numpy as np
import pandas as pd


class History(object):

    session = models.Session()

    def get_history_by_base_currency(self, currency_id):
        return self.session.query(models.History).join(models.History.base_currency).filter(models.History.base_currency_id == currency_id).all()

    def get_all(self):
        #return self.session.query(models.History).join(models.History.base_currency).all()
        query = self.session.query(models.History).join(models.History.base_currency)
        return pd.read_sql(query.statement, self.session.bind)

    def get_all_base_currency_from_history(self):
        base_currencies = self.session.query(models.History).group_by(models.History.base_currency_id).all()
        currency_dict = dict()
        for item in base_currencies:
            currency_dict[item.base_currency_id] = item
        return currency_dict
        #return self.session.query(models.History).group_by(models.History.base_currency_id).all()