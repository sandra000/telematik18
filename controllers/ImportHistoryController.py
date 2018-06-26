import models
import numpy as np
import pandas as pd


class ImportHistory(object):

    session = models.Session()

    def get_Exchanges(self):
        query = "SELECT * FROM Mark"#self.session.query(models.Mark)
        return pd.read_sql(query.statement, self.session.bind)
