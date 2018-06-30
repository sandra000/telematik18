import models
import numpy as np
import pandas as pd


class Cryptocurrency(object):

    session = models.Session()

    def get_all(self):
        query = self.session.query(models.Cryptocurrency)
        return pd.read_sql(query.statement, self.session.bind)

    def get_base_filtert(self,Currency_Pattern="%"):
        return self.session.execute('SELECT DISTINCT name_id FROM cryptocurrencies INNER JOIN Symbols ON cryptocurrencies.id=Symbols.base_cryptocurrency_id WHERE symbol_global_id like \''+Currency_Pattern+'\' ORDER BY name_id')

    def get_quote_filtert(self,Currency_Pattern="%"):
        return self.session.execute('SELECT DISTINCT name_id FROM cryptocurrencies INNER JOIN Symbols ON cryptocurrencies.id=Symbols.quote_cryptocurrency_id WHERE symbol_global_id like \''+Currency_Pattern+'\' ORDER BY name_id')