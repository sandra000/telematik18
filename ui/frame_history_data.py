import tkinter as tk
from pandastable import Table, TableModel
from controllers import History


class HistoryDataFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        df = self.get_history()
        tb_m = TableModel(dataframe=df)
        table = Table(self, model=tb_m)
        table.show()
        #alter the DataFrame in some way, then update
        table.redraw()

    def get_history(self):
        history = History()
        return history.get_all()
