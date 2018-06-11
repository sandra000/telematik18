import tkinter as tk
from pandastable import Table, TableModel
from controllers import Cryptocurrency


class CryptocurrencyDataFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        df = self.get_cryptocurrency()
        tbM = TableModel(dataframe=df)
        table = Table(self, model=tbM)
        table.show()
        table.redraw()

    def get_cryptocurrency(self):
        cryptocurrency = Cryptocurrency()
        return cryptocurrency.get_all()
