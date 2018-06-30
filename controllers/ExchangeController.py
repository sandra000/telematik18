import models
import numpy as np
import pandas as pd


class Exchange(object):

    session = models.Session()

    def get_all(self): 
        query = self.session.query(models.Mark)
        return pd.read_sql(query.statement, self.session.bind)

    def get_filtert(self,Currency_Pattern="%"):
        return self.session.execute('SELECT DISTINCT exchange_global_id FROM Marks INNER JOIN Symbols ON marks.id=symbols.mark_id WHERE symbol_global_id like \''+Currency_Pattern+'\' ORDER BY exchange_global_id')
