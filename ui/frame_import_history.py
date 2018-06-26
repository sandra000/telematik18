import tkinter as tk
from pandastable import Table, TableModel
from controllers import ImportHistory


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

        #Select Exchange
        selectedExchange = tk.StringVar(self)
        exchanges={'1','2','3'}#get_exchanges(self)
        popupMenu = tk.OptionMenu(self, selectedExchange, *exchanges)
        popupMenu.pack()
        #tk.Label(mainframe, text="Choose Exchange").grid(row = 1, column = 1)
        #popupMenu.grid(row = 2, column =1)

    # on change dropdown value
    def change_dropdown(*args):
        print(selectedExchange)
    def get_exchanges(self):
        exchangeNames=ImportHistory.get_Exchanges
        result.set()
        for i in range(0,len(ExchangeNames)-1):
            result.add(exchangeNames[i])
        if len(ExchangeNames)>0:
            selectedExchange.set(exchangeNames[0])
        else:
            selectedExchange.set('No Markets imported')
        return result
