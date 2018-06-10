import tkinter as tk
from pandastable import Table, TableModel
import pandas as pd


class CorrelationFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #button2 = tk.Button(self, text="Disagree", command=quit)
        #button2.pack()
        d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'caaaa']),
             'two': pd.Series([1., 2., 3.], index=['a', 'b', 'caaaa'])}
        df = pd.DataFrame(d)
        tbM = TableModel(dataframe=df)
        table = Table(self, model=tbM)
        table.show()
        #alter the DataFrame in some way, then update
        table.redraw()