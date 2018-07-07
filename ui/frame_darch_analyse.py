import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from controllers import HistoryController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from arch import arch_model


class DARCHFrame(tk.Frame):
    figureCorelation = plt.figure()
    valor = tk.StringVar()
    test_var = tk.IntVar()
    symbol_selected = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # set the grid size
        col = 0
        while col < 12:
            self.columnconfigure(col, weight=1)
            col += 1
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        label = tk.Label(self, text="Darch", font=controller.LARGE_FONT)
        label.grid(row=0, columnspan=12)

        self.a = self.figureCorelation.add_subplot(111)

        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()

        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=1, column=11, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)

        btn_update_selected = tk.Button(self, text="Update", command=self.renew)
        btn_update_selected.grid(row=4, column=11)

    def update(self):

        self.a.cla()  # which clears data but not axes

        symbol_selected = self.symbol_selected
        bitcoin_name = "BITSTAMP_SPOT_BTC_USD"

        # for the first time we will compare all currencies with bitcoin as base currency
        base_symbol = list(filter(lambda x: x.symbol_global_id == bitcoin_name, self.symbol_data))[0]

        history = HistoryController.History()

        # draw base history base currency/symbol data
        history_data = history.get_by_symbol_id(base_symbol.id)
        if history_data.values.size == 0:
            return
        figure = self.figureCorelation
        if len(symbol_selected):
            for item in symbol_selected:
                # TODO: only for one
                # TODO: change data to be with Datum
                current_history_data = history.get_by_symbol_id(item.id)

                # dropna() - entfernt die leere Daten
                # pct_change(12) - wie vie jeder Wert prozentual geändert wurde, von der Mitte und mir dem Schritt 12 gerechnet
                current_prices = 100 * current_history_data.ask_price.pct_change(12).dropna()
                am = arch_model(current_prices)
                res = am.fit(update_freq=5)
                # TODO: output this to frame
                print(res.summary())
                figure = res.plot()
                #self.a.plot(res, color='red', label=bitcoin_name)

                # ar = ARX(ann_inflation, lags=[1, 3, 12])
                # print(ar.fit().summary()
                # ar.volatility = ARCH(p=5)
                # res = ar.fit(update_freq=0, disp='off')
                # print(res.summary())
                # fig = res.plot()

        self.a.legend()

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().grid(row=1, rowspan=3, columnspan=11, sticky=(tk.N, tk.S, tk.E, tk.W))
        canvas.draw()

        toolbar_frame = tk.Frame(master=self)
        toolbar_frame.grid(row=4, columnspan=11, sticky=tk.W)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        return True

    def renew(self):
        self.symbol_selected = self.symbol_list.get_selection()
        self.update()


class SymbolList(tk.Frame):

    def __init__(self, parent, symbols):
        tk.Frame.__init__(self, parent)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        # prepare data for listbox
        self.symbol_dict = dict()
        for item in symbols:
            self.symbol_dict[item.symbol_global_id] = item

        for key in self.symbol_dict:
            self.listbox.insert(tk.END, key)

    def get_selection(self):
        return_list = list()
        for key in self.listbox.selection_get().split():
            return_list.append(self.symbol_dict[key])
        return return_list
