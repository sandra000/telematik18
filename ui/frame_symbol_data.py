import tkinter as tk
from pandastable import Table, TableModel
from controllers import Symbol


class SymbolDataFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        df = self.get_symbol()
        tb_m = TableModel(dataframe=df)
        table = Table(self, model=tb_m)
        table.show()
        table.redraw()

    def get_symbol(self):
        symbol = Symbol()
        return symbol.get_all()
