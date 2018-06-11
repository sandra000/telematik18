import tkinter as tk
from pandastable import Table, TableModel
from controllers import Exchange


class ExchangeDataFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        df = self.get_exchange()
        tbM = TableModel(dataframe=df)
        table = Table(self, model=tbM)
        table.show()
        table.redraw()

    def get_exchange(self):
        exchange = Exchange()
        return exchange.get_all()
