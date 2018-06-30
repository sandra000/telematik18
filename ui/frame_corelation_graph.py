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
        label = tk.Label(self, text="Corelation graph", font=controller.LARGE_FONT)
        label.pack(pady=5,padx=5)
        self.a = self.figureCorelation.add_subplot(111)
        symbol = SymbolController.Symbol()
        symboldata = symbol.get_all_as_list()
        for symbol in symboldata:
            item = SymbolSelect()
            item.var = tk.BooleanVar(self)
            item.symbol_global_id = symbol.symbol_global_id
            self.symbol_selected_list.append(item)

    def update(self):
        bitcoin_name = 1
        etherum_name = 3
        zcash_name = 17

        mb = tk.Menubutton(self, text="Select the markets/curecnies", relief=tk.RAISED)
        mb.pack(side=tk.RIGHT)
        mb.menu = tk.Menu(mb, tearoff=0)
        mb["menu"] = mb.menu

        for short_symbol in self.symbol_selected_list:
            mb.menu.add_checkbutton(label=short_symbol.symbol_global_id, variable=short_symbol.var)

#TODO create separate frame
        # scrollbar = tk.Scrollbar(self)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        #
        # listbox = tk.Listbox(self)
        # listbox.pack()
        #
        # listbox.config(yscrollcommand=scrollbar.set)
        # scrollbar.config(command=listbox.yview)
        #
        #
        # for short_symbol in self.symbol_selected_list:
        #     listbox.insert(tk.END, short_symbol.symbol_global_id)

        symbol_list = SymbolList(self, self.symbol_selected_list)
        symbol_list.pack(side=tk.RIGHT, fill=tk.X)
        symbol_list.config(relief=tk.GROOVE, bd=2)

        btn_show_selected = tk.Button(self, text="Print selected", command=self.item_test)
        btn_show_selected.pack(side=tk.RIGHT)


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
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



        # dialog_button = tk.Button(self, text="test", command=lambda: self.dialogo())
        # dialog_button.pack(side='right')

        return True

    # def dialogo(self):
    #     d = MyDialog(self, self.valor, "Select the parameter", "Select")
    #     self.wait_window(d.top)

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


# class MyDialog(tk.Frame):
#     def __init__(self, parent, valor, title, labeltext='', list_of_symbol_var=[]):
#         self.valor = valor
#
#         self.top = tk.Toplevel(parent)
#         self.top.transient(parent)
#         self.top.grab_set()
#         if len(title) > 0: self.top.title(title)
#         if len(labeltext) == 0: labeltext = 'Valor'
#         tk.Label(self.top, text=labeltext).pack()
#         self.top.bind("<Return>", self.ok)
#         self.e = tk.Entry(self.top, text=valor.get())
#         self.e.bind("<Return>", self.ok)
#         self.e.bind("<Escape>", self.cancel)
#         self.e.pack(padx=15)
#         self.e.focus_set()
#         b = tk.Button(self.top, text="OK", command=self.ok)
#         b.pack(pady=5)
#
#
#         mb = tk.Menubutton(self.top, text="CheckComboBox", relief=tk.RAISED)
#         mb.pack()
#         mb.menu = tk.Menu(mb, tearoff=0)
#         mb["menu"] = mb.menu
#
#         self.Item0 = tk.IntVar(self)
#         self.Item1 = tk.IntVar(self)
#         self.Item2 = tk.IntVar(self)
#
#         mb.menu.add_checkbutton(label="Item0", variable=self.Item0)
#         mb.menu.add_checkbutton(label="Item1", variable=self.Item1)
#         mb.menu.add_checkbutton(label="Item2", variable=self.Item2)
#
#         button1 = tk.Button(self, text="Item True/False Test", command=self.item_test)
#         button1.pack()
#         # for var in list_of_symbol_vars:
#         #     tk.Checkbutton(self, text="male", variable=var).grid(row=0, sticky=W)
#
#     def ok(self, event=None):
#         print("Has escrito ...", self.e.get())
#         self.valor.set(self.e.get())
#         self.top.destroy()
#
#
#     def cancel(self, event=None):
#         self.top.destroy()
#
#     def item_test(self):
#         print(self.Item0.get())
#         print(self.Item1.get())
#         print(self.Item2.get())


class SymbolList(tk.Frame):

    def __init__(self, parent, symbol_selected_list, picks=[], side=tk.LEFT, anchor=tk.W):
        tk.Frame.__init__(self, parent)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        listbox.pack()

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        for short_symbol in symbol_selected_list:
            listbox.insert(tk.END, short_symbol.symbol_global_id)


# class Checkbar(tk.Frame):
#     # self.selected_symbols = Checkbar(self,
#     #                                  ['BITSTAMP_SPOT_BTC_USD', 'BITSTAMP_SPOT_ETH_USD', 'BITSTAMP_SPOT_LTC_USD',
#     #                                   ])
#     #    self.selected_symbols.pack(side='top', fill='x')
#     #    self.selected_symbols.config(relief='groove', bd=2)
#
#     vars = []
#
#     def __init__(self, parent, picks=[], side=tk.LEFT, anchor=tk.W):
#         tk.Frame.__init__(self, parent)
#         self.test_var = tk.BooleanVar(self)
#         for pick in picks:
#             var = tk.BooleanVar(self)
#             chk = tk.Checkbutton(self, text=pick, variable=var)
#             chk.pack(side=side)
#             self.vars.append(var)
#         chk = tk.Checkbutton(self, text='test2', variable=self.test_var)
#         chk.pack()
#
#     def state(self):
#         print("Has escrito ...", self.test_var.get())
#         return map((lambda var: var.get()), self.vars)
#
#     def ok(self, event=None):
#         print("Has escrito ...", self.test_var.get())
