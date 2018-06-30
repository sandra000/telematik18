import tkinter as tk
from pandastable import Table, TableModel
from controllers import Exchange


class ImportHistoryFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #df = self.get_exchange()
        #tb_m = TableModel(dataframe=df)
        #table = Table(self, model=tb_m)
        #table.show()
        #table.redraw()
        w = tk.Label(self, text="Import History")
        w.pack()
        w = tk.Label(self, text="Exchange")
        w.pack()
        exchangeClontroller=Exchange()
        #Select Exchange
        selectedExchange = tk.StringVar(self)
        exchanges=self.get_exchanges(exchangeClontroller,selectedExchange)
        popupMenu = tk.OptionMenu(self, selectedExchange, *exchanges)
        popupMenu.pack()
        #tk.Label(mainframe, text="Choose Exchange").grid(row = 1, column = 1)
        #popupMenu.grid(row = 2, column =1)

        # on change dropdown value
    def change_dropdown(self, *args):
        print(selectedExchange)
    def get_exchanges(self,exchangeClontroller,selectedExchange):
        exchangeNames=exchangeClontroller.get_all()
        result=set()
        for i in range(0,len(exchangeNames)-1):
            result.add(exchangeNames.name[i])
        if len(exchangeNames)>0:
            selectedExchange.set(exchangeNames.name[0])
        else:
            selectedExchange.set('No Markets imported')
        return result
