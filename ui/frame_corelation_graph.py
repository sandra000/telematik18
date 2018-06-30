import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from controllers import HistoryController, SymbolController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


# naked object
class SymbolSelect(object):
    pass


class CorrelationGraphFrame(tk.Frame):
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
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        label = tk.Label(self, text="Corelation graph", font=controller.LARGE_FONT)
        label.grid(row=0, columnspan=12)

        self.a = self.figureCorelation.add_subplot(111)

        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()

        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=1, column=11, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)

        btn_update_selected = tk.Button(self, text="Update", command=self.renew)
        btn_update_selected.grid(row=2, column=11)

    def update(self):

        self.a.cla()  # which clears data but not axes
        #self.a.clf()  # which clears data and axes

        symbol_selected = self.symbol_selected
        bitcoin_name = "BITSTAMP_SPOT_BTC_USD"

        # for the first time we will compare all currencies with bitcoin as base currency
        base_symbol = list(filter(lambda x: x.symbol_global_id == bitcoin_name, self.symbol_data))[0]

        history = HistoryController.History()

        # draw base history base currency/symbol data
        history_data = history.get_by_symbol_id(base_symbol.id)
        if history_data.values.size == 0:
            return
        self.a.plot(history_data.ask_price.values, color='red', label=bitcoin_name)

        if len(symbol_selected):
            base_max_price = history_data.ask_price.max()
            for item in symbol_selected:
                current_history_data = history.get_by_symbol_id(item.id)
                current_max_price = current_history_data.ask_price.max()
                coefficient_diff = base_max_price / current_max_price
                current_price_normalise = current_history_data.ask_price.mul(coefficient_diff).values
                self.a.plot(current_price_normalise, label=item.symbol_global_id)

        self.a.legend()

        canvas = FigureCanvasTkAgg(self.figureCorelation, self)
        canvas.get_tk_widget().grid(row=1, columnspan=11, sticky=(tk.N, tk.S, tk.E, tk.W))
        canvas.draw()

        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row=2, columnspan=11, sticky=tk.W)
        toolbar = NavigationToolbar2TkAgg(canvas, toolbarFrame)
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
