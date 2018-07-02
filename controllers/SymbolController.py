import models
import numpy as np
import pandas as pd


class Symbol(object):

    session = models.Session()

    def get_all(self):
        query = self.session.query(models.Symbol)
        return pd.read_sql(query.statement, self.session.bind)

    def get_all_as_list(self):
        return self.session.query(models.Symbol).all()