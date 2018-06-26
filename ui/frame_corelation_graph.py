import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pandastable import Table, TableModel
from controllers import HistoryController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


class CorrelationGraphFrame(tk.Frame):
    figureCorelation = plt.figure()
    valor = tk.StringVar()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Corelation graph", font=controller.LARGE_FONT)
        label.pack(pady=5,padx=5)
        button444 = tk.Button(self, text="test", command=lambda: self.dialogo())
        button444.pack(side='right')

        a = self.figureCorelation.add_subplot(111)

        #TODO: fix this
        bitcoin_name = 1
        etherum_name = 3
        zcash_name = 17
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
        a.plot(historydata_grouped.get_group(bitcoin_name).ask_price.values, color='red', label='bitcoin')
        a.plot(etherum_ask_price_normalise, color='blue', label='ethereum')
        #plot(bitcoin_name, etherum_name, data=historydata_grouped)
        #matplotlib.pyplot.annotate(*args, **kwargs)
        #matplotlib.pyplot.arrow(x, y, dx, dy, hold=None, **kwargs)¶

        canvas = FigureCanvasTkAgg(self.figureCorelation, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.valor.set("Hola Manejando datos")  # ?????? why we need this
        tk.Label(self, textvariable=self.valor).pack()

        # for pick in picks:
        #     var = tk.IntVar()
        #     self.vars.append(var)
        self.selected_symbols = Checkbar(self,
                                         ['BITSTAMP_SPOT_BTC_USD', 'BITSTAMP_SPOT_ETH_USD', 'BITSTAMP_SPOT_LTC_USD',
                                          'BITSTAMP_SPOT_XRP_USD', 'KRAKEN_SPOT_ZEC_USD', 'KRAKEN_SPOT_BTC_USD',
                                          'KRAKEN_SPOT_DASH_USD'])
        self.selected_symbols.pack(side='top', fill='x')
        self.selected_symbols.config(relief='groove', bd=2)
        self.test_var = tk.IntVar()
        side = 'left',
        anchor = 'w'
        chk = tk.Checkbutton(self, text='test', variable=self.test_var, command=self.cb())
        chk.pack(side=side, anchor=anchor, expand='yes')

    def cb(self):
        print
        "variable is", self.test_var.get()

    def update(self):
        return True

    def dialogo(self):
        print(list(self.selected_symbols.state()))
        print(self.test_var.get())

        # d = MyDialog(self, self.valor, "Select the parameter", "Select")
        # self.wait_window(d.top)
        # self.valor.set(d.ejemplo)

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


class MyDialog(tk.Frame):
    def __init__(self, parent, valor, title, labeltext='', list_of_symbol_var=[]):
        self.valor = valor

        self.top = tk.Toplevel(parent)
        self.top.transient(parent)
        self.top.grab_set()
        if len(title) > 0: self.top.title(title)
        if len(labeltext) == 0: labeltext = 'Valor'
        tk.Label(self.top, text=labeltext).pack()
        self.top.bind("<Return>", self.ok)
        self.e = tk.Entry(self.top, text=valor.get())
        self.e.bind("<Return>", self.ok)
        self.e.bind("<Escape>", self.cancel)
        self.e.pack(padx=15)
        self.e.focus_set()
        b = tk.Button(self.top, text="OK", command=self.ok)
        b.pack(pady=5)



        # for var in list_of_symbol_vars:
        #     tk.Checkbutton(self, text="male", variable=var).grid(row=0, sticky=W)

    def ok(self, event=None):
        print("Has escrito ...", self.e.get())
        self.valor.set(self.e.get())
        self.top.destroy()


    def cancel(self, event=None):
        self.top.destroy()


class Checkbar(tk.Frame):

    def __init__(self, parent=None, picks=[], side='left', anchor='w'):
        tk.Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand='yes')
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)
