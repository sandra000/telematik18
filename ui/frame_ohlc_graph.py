import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pandastable import Table, TableModel
from controllers import HistoryController
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#Technical analysts can use autocorrelation to see how much of an impact past prices for a security have on
# its future price
#Assume an investor is looking to discern if a stock's returns in her portfolio exhibit autocorrelation; the
# stock's returns are related to its returns in previous trading sessions. If the returns do exhibit autocorrelation,
# the stock could be characterized as a momentum stock; its past returns seem to influence its future returns.
# The investor runs a regression with two prior trading sessions' returns as the independent variables and the current
# return as the dependent variable. She finds that returns one day prior have a positive autocorrelation of 0.7, while
# the returns two days prior have a positive autocorrelation of 0.3. Past returns seem to influence future returns, and
# she can adjust her portfolio to take advantage of the autocorrelation and resulting momentum.



class OhlcGraphFrame(tk.Frame):
    figureOhlcChart = plt.figure()
    valor = tk.StringVar()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="BTC Candlestick Chart", font=controller.LARGE_FONT)
        label.pack(pady=5,padx=5)
        self.a = self.figureOhlcChart.add_subplot(111)

    def on_show(self):
        self.update()

    def update(self):
        # TODO: fix this
        bitcoin_name = 1
        etherum_name = 3
        zcash_name = 17
        history = HistoryController.History()  # object for the databank endpoint
        historydata = history.get_all()  # dataframe
        if historydata.values.size == 0:
            return
        historydata_grouped = historydata.groupby('base_currency_id') #symbol_id

        df = historydata_grouped.get_group(bitcoin_name)
        df['date'] = df['start_time_exchange'].map(mdates.date2num)
        df = df.loc[df['symbol_id'] == 16]
        ohlc = df[['date', 'ask_price', 'ask_price_high', 'ask_price_low', 'ask_price_last']]
        candlestick_ohlc(self.a, ohlc.values, width=.6, colorup='green', colordown='red')
        self.a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

        #moving averages
        df['ema20'] = df['ask_price_last'].ewm(span=20, adjust=False).mean()
        df['ema50'] = df['ask_price_last'].ewm(span=50, adjust=False).mean()

        # correct for starting period errors
        #df = df[df.index > '2015-5-31']

        self.a.plot(df['date'], df['ema20'], color='blue', label='Moving Average 20 days')
        self.a.plot(df['date'], df['ema50'], color='purple', label='Moving Average 50 days')

        self.a.grid(False)
        self.a.legend()

        canvas = FigureCanvasTkAgg(self.figureOhlcChart, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        return True

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
