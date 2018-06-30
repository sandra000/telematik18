import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pandastable import Table, TableModel
from controllers import HistoryController, SymbolController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

# naked object
class SymbolSelect(object):
    pass

class CorrelationGraphFrame(tk.Frame):
    figureCorelation = plt.figure()
    valor = tk.StringVar()
    test_var = tk.IntVar()
    symbol_selected_list = []

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

        # for symbol in symboldata:
        #     item = SymbolSelect()
        #     item.var = tk.BooleanVar(self)
        #     item.symbol_global_id = symbol.symbol_global_id
        #     self.symbol_selected_list.append(item)

    def update(self):
        bitcoin_name = 1
        etherum_name = 3
        zcash_name = 17

        symbol_list = SymbolList(self, self.symbol_data)
        symbol_list.grid(row=1, column=11, sticky=(tk.N, tk.S, tk.E, tk.W))
        symbol_list.config(relief=tk.GROOVE, bd=2)
        symbol_list.print_selected()

        btn_show_selected = tk.Button(self, text="Update", command=symbol_list.print_selected)
        btn_show_selected.grid(row=2, column=11)

#Update graph
        history = HistoryController.History()
        historydata = history.get_all()
        if historydata.values.size == 0:
            return
        historydata_grouped = historydata.groupby('base_currency_id')
        bitcoin_max_price = historydata_grouped.get_group(bitcoin_name).ask_price.max()
        etherum_max_price = historydata_grouped.get_group(etherum_name).ask_price.max()
        zcash_max_price = historydata_grouped.get_group(zcash_name).ask_price.max()
        coeficeint_diff = bitcoin_max_price / etherum_max_price
        coeficeint_diff2 = bitcoin_max_price / zcash_max_price
        etherum_ask_price_normalise = historydata_grouped.get_group(etherum_name).ask_price.mul(coeficeint_diff).values
        self.a.plot(historydata_grouped.get_group(bitcoin_name).ask_price.values, color='red', label='bitcoin')
        self.a.plot(etherum_ask_price_normalise, color='blue', label='ethereum')
        self.a.legend()
        # plot(bitcoin_name, etherum_name, data=historydata_grouped)
        # matplotlib.pyplot.annotate(*args, **kwargs)
        # matplotlib.pyplot.arrow(x, y, dx, dy, hold=None, **kwargs)

        canvas = FigureCanvasTkAgg(self.figureCorelation, self)
#        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().grid(row=1, columnspan=11, sticky=(tk.N, tk.S, tk.E, tk.W))
        canvas.draw()

        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row=2, columnspan=11, sticky=tk.W)
        toolbar = NavigationToolbar2TkAgg(canvas, toolbarFrame)
        toolbar.update()

        return True

    def item_test(self):
        for symbol in self.symbol_selected_list:
            print(symbol.var.get())

    def get_correlation(self):
        #TODO: sort the history list
        history = HistoryController.History()
        historydata = history.get_all()
        all_base_cuurencies = history.get_all_base_currency_from_history()
        historydata_grouped = historydata.groupby('base_currency_id')
        currency_list = []
        for item in all_base_cuurencies:
            currency_list.append(all_base_cuurencies[item].base_currency.name)
        output_pd = pd.DataFrame(index=currency_list, columns=currency_list)
        for name, group in historydata_grouped:
            currency_name = all_base_cuurencies[name].base_currency.name
            main_currency_arr = group.ask_price.values
            output_arr = []
            for name2, group2 in historydata_grouped:
                tmp_main_currency_arr = main_currency_arr
                current_currency_arr = group2.ask_price.values
                if current_currency_arr.size > main_currency_arr.size:
                    current_currency_arr = np.resize(current_currency_arr, main_currency_arr.shape)
                if current_currency_arr.size < main_currency_arr.size:
                    tmp_main_currency_arr = np.resize(main_currency_arr, current_currency_arr.shape)
                coef = np.corrcoef(tmp_main_currency_arr, current_currency_arr)
                output_arr.append(coef[0,1])
            output_pd.loc[currency_name] = output_arr
        return output_pd


class SymbolList(tk.Frame):

    def __init__(self, parent, symbol_selected_list, picks=[], side=tk.LEFT, anchor=tk.W):
        tk.Frame.__init__(self, parent)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        for short_symbol in symbol_selected_list:
            self.listbox.insert(tk.END, short_symbol.symbol_global_id)

    def print_selected(self):
        print(self.listbox.curselection())
