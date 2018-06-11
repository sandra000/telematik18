import tkinter as tk
from pandastable import Table, TableModel
import pandas as pd
from controllers import HistoryController

class CorrelationFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #button2 = tk.Button(self, text="Disagree", command=quit)
        #button2.pack()
        d = {'one': pd.Series([1., 2., 4.], index=['a', 'b', 'caaaa']),
             'two': pd.Series([1., 2., 3.], index=['a', 'b', 'caaaa'])}
        df = pd.DataFrame(d)
        df2 = self.get_correlation()
        tbM = TableModel(dataframe=df2)
        table = Table(self, model=tbM)
        table.show()
        #alter the DataFrame in some way, then update
        table.redraw()

    def get_correlation(self):
        history = HistoryController.History()
        return history.get_all_history()
        all_base_cuurencies = history.get_all_base_currency_from_history()
        symbols = session.query(models.Symbol).filter(models.Symbol.symbol_global_id == symbol_global_id).all()
        if len(symbols) > 0:
            symbol_id = symbols[0].id
            result = session.query(models.History).filter(models.History.symbol_id == symbol_id).all()
            return result

#   df = pd.read_sql(sql_command, engine)
