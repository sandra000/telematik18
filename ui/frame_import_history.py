import tkinter as tk
import datetime
from pandastable import Table, TableModel
from controllers import Exchange
from controllers import Cryptocurrency
from api import MainImport


class ImportHistoryFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Set the grid size
        col = 0
        while col < 12:
            self.columnconfigure(col, weight=1)
            col += 1
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=5)

        #df = self.get_exchange()
        #tb_m = TableModel(dataframe=df)
        #table = Table(self, model=tb_m)
        #table.show()
        #table.redraw()
        
        w = tk.Label(self, text="Import History")
        w.grid(row=0, columnspan=12)
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
        self.importAPI=MainImport()
   
    def draw_elements(self):
        #Select Exchange
        self.popupMenu = tk.OptionMenu(self, self.selectedExchange, *self.exchanges,  command=self.change_dropdown_exchange) 
        self.popupMenu.grid(row=1, column=5, columnspan=2, sticky=(tk.N))
        #Select Base Cur
        w1 = tk.Label(self, text="Base currency")
        w1.grid(row=2, column=4, sticky=(tk.N, tk.E))
        self.popupMenu2 = tk.OptionMenu(self, self.selectedBaseCur, *self.baseCurs,  command=self.change_dropdown_base_cur)
        self.popupMenu2.grid(row=2, column=5, sticky=(tk.N, tk.W))
        #Select QuoteCur
        w2 = tk.Label(self, text="Quote currency")
        w2.grid(row=2, column=6, sticky=(tk.N, tk.E))
        self.popupMenu3 = tk.OptionMenu(self, self.selectedQuoteCur, *self.quoteCurs,  command=self.change_dropdown_quote_cur)
        self.popupMenu3.grid(row=2, column=7, sticky=(tk.N, tk.W))
        #Select Period
        self.popupMenu4 = tk.OptionMenu(self, self.selectedPeriod, *self.periods)
        self.popupMenu4.grid(row=3, column=5, columnspan=2, sticky=(tk.N))
        #Datum
        fromDate = tk.StringVar(self)
        fromDateField = tk.Entry(self, textvariable=fromDate)
        fromDate.set("01.01.2018")
        s = fromDate.get()

        toDate = tk.StringVar(self)
        toDateField = tk.Entry(self, textvariable=toDate)
        toDate.set("01.06.2018")
        s = toDate.get()

        w1 = tk.Label(self, text="From date")
        w1.grid(row=4, column=4, sticky=(tk.N, tk.E))
        fromDateField.grid(row=4, column=5, sticky=(tk.N, tk.W))
        w2 = tk.Label(self, text="To date")
        w2.grid(row=4, column=5, sticky=(tk.N, tk.E))
        toDateField.grid(row=4, column=6, sticky=(tk.N, tk.W))

        #Import-Button
        self.button = tk.Button(self, text="Import", width=10, command=self.start_import)
        self.button.grid(row=5, column=5, columnspan=2, sticky=(tk.N))

        #print(cal.selection_get())
        
        #self.startDate=datetime.datetime.now()
        #self.calStart = tk.ttk. .Calendar(self, font="Arial 14", selectmode='day', cursor="hand1",year=self.startDate.year, month=self.startDate.month, day=self.startDate.day)
        #self.calStart.pack(fill="both", expand=True)

    def remove_elements(self):
        self.popupMenu.destroy()
        self.popupMenu2.destroy()
        self.popupMenu3.destroy()
        self.popupMenu4.destroy()
        self.button.destroy()
    def start_import(self):
        #importiert wird ab dem 1.1.2018, maximal jedoch 10000 Einträge
        symbol=self.selectedExchange.get() + "_SPOT_" + self.selectedBaseCur.get() + "_" + self.selectedQuoteCur.get()
        self.importAPI.update_ohcl_histories(symbol,self.selectedPeriod.get())
        
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
