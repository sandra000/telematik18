import models
import numpy as np
import pandas as pd


class Exchange(object):

    session = models.Session()

    def get_all(self):
        query = self.session.query(models.Mark)
        return pd.read_sql(query.statement, self.session.bind)
