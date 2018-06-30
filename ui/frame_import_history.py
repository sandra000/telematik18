import tkinter as tk
from pandastable import Table, TableModel
from controllers import Exchange
from controllers import Cryptocurrency


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
        #w = tk.Label(self, text="Exchange")
        #w.pack()
        self.exchangeController=Exchange()
        self.currencyController=Cryptocurrency()
        #Exchange
        self.selectedExchange = tk.StringVar(self)
        self.exchanges=list()#set()#self.get_exchanges()
        #BaseCur
        self.selectedBaseCur = tk.StringVar(self)
        self.baseCurs=list()
        #QuoteCur
        self.selectedQuoteCur = tk.StringVar(self)
        self.quoteCurs=list()
        self.load_defaults()
        #static data
        self.periods=['1SEC', '2SEC', '3SEC', '4SEC', '5SEC', '6SEC', '10SEC', '15SEC', '20SEC', '30SEC', '1MIN', '2MIN', '3MIN', '4MIN', '5MIN', '6MIN', '10MIN', '15MIN', '20MIN', '30MIN', '1HRS', '2HRS', '3HRS', '4HRS', '6HRS', '8HRS', '12HRS', '1DAY', '2DAY', '3DAY', '5DAY', '7DAY', '10DAY', '1MTH', '2MTH', '3MTH', '4MTH', '6MTH', '1YRS', '2YRS', '3YRS', '4YRS', '5YRS']
        self.selectedPeriod=tk.StringVar(self)
        self.selectedPeriod.set('1DAY')
        self.draw_elements()

   
    def draw_elements(self):
        #Select Exchange
        self.popupMenu = tk.OptionMenu(self, self.selectedExchange, *self.exchanges,  command=self.change_dropdown_exchange)
        self.popupMenu.pack()
        #Select Base Cur
        self.popupMenu2 = tk.OptionMenu(self, self.selectedBaseCur, *self.baseCurs,  command=self.change_dropdown_base_cur)
        self.popupMenu2.pack()
        #Select QuoteCur
        self.popupMenu3 = tk.OptionMenu(self, self.selectedQuoteCur, *self.quoteCurs,  command=self.change_dropdown_quote_cur)
        self.popupMenu3.pack()
        #Select Period
        self.popupMenu4 = tk.OptionMenu(self, self.selectedPeriod, *self.periods)
        self.popupMenu4.pack()
        #Import-Button
        self.button = tk.Button(self, text="Import", width=10, command=self.start_import)
        self.button.pack()

    def remove_elements(self):
        self.popupMenu.destroy()
        self.popupMenu2.destroy()
        self.popupMenu3.destroy()
        self.popupMenu4.destroy()
        self.button.destroy()
    def start_import(self):
        print(self.selectedExchange.get())
        
    def change_dropdown_exchange(self, *args):
        self.get_base_curs()
        self.get_quote_curs()
        self.remove_elements()
        self.draw_elements()

    def change_dropdown_base_cur(self, *args):
        self.get_exchanges()
        self.get_quote_curs()
        self.remove_elements()
        self.draw_elements()

    def change_dropdown_quote_cur(self, *args):
        self.get_exchanges()
        self.get_base_curs()
        self.remove_elements()
        self.draw_elements()
        
    def load_defaults(self):
        self.selectedExchange.set('Select Exchange')
        self.selectedBaseCur.set('Select Currency')
        self.selectedQuoteCur.set('Select Currency')
        self.get_exchanges()
        self.get_base_curs()
        self.get_quote_curs()
        
    def get_exchanges(self):
        filter=""
        if self.selectedBaseCur.get()=='Select Currency':
            filter="%_"
        else:
            filter="%_"+self.selectedBaseCur.get()+"_"
        if self.selectedQuoteCur.get()=='Select Currency':
            filter=filter+"%"
        else:
            filter=filter+self.selectedQuoteCur.get()

        exchangeNames=self.exchangeController.get_filtert(filter)
        self.exchanges.clear()
        self.exchanges.append('Select Exchange')
        for ex in exchangeNames:
            self.exchanges.append(ex[0])

    def get_base_curs(self):
        filter=""
        if self.selectedExchange.get()=='Select Exchange':
            filter="%"
        else:
            filter=self.selectedExchange.get()+"_%"
        if self.selectedQuoteCur.get()=='Select Currency':
            filter=filter #nichts verändern
        else:
            filter=filter+self.selectedQuoteCur.get()

        currencys=self.currencyController.get_base_filtert(filter)
        self.baseCurs.clear()
        self.baseCurs.append('Select Currency')
        for cur in currencys:
            self.baseCurs.append(cur[0])

    def get_quote_curs(self):
        filter=""
        if self.selectedExchange.get()=='Select Exchange':
            filter="%"
        else:
            filter=self.selectedExchange.get()+"_%"
        if self.selectedBaseCur.get()=='Select Currency':
            filter=filter #nichts verändern
        else:
            filter=filter+"_"+self.selectedBaseCur.get()+"_%"

        currencys=self.currencyController.get_quote_filtert(filter)
        self.quoteCurs.clear()
        self.quoteCurs.append('Select Currency')
        for cur in currencys:
            self.quoteCurs.append(cur[0])
