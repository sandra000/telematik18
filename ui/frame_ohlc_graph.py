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
from ui.components import SettingView, ParameterList, SymbolList


class OhlcGraphFrame(tk.Frame):
    figureOhlcChart = plt.figure()
    valor = tk.StringVar()
    symbol_selected = []
    parameter = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        col = 0
        while col < 12:
            self.columnconfigure(col, weight=1)
            col += 1
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        label = tk.Label(self, text="BTC Candlestick Chart", font=controller.LARGE_FONT)
        label.grid(row=0, columnspan=12)

        self.a = self.figureOhlcChart.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figureOhlcChart, self)
        self.canvas.get_tk_widget().grid(row=1, rowspan=3, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()
        self.parameters = history.get_all_parameter_from_history()

        self.setting_view = SettingView(self)
        self.setting_view.grid(row=1, column=10, sticky=(tk.N, tk.E))

        self.parameter_list = ParameterList(self, self.parameters)
        self.parameter_list.grid(row=1, column=11, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.parameter_list.config(relief=tk.GROOVE, bd=2)

        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=2, column=10, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)

        btn_update_selected = tk.Button(self, text="Update", command=self.renew)
        btn_update_selected.grid(row=4, column=10, columnspan=2)

    def on_show(self):
        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()
        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=2, column=10, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)
        self.update()

    def update(self):
        self.a.cla()

        symbol_selected = self.symbol_selected
        history = HistoryController.History()

        if not self.parameter:
            return

        if len(symbol_selected):
            self.setting_view.update_view(parameter=self.parameter, symbols=symbol_selected)
            for item in symbol_selected:

                df = history.get_by_symbol_id_and_parameter_id(item.id, self.parameter.id)
                df['date'] = df['start_time_exchange'].map(mdates.date2num)



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

        self.canvas.get_tk_widget().grid(row=1, rowspan=3, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        toolbar_frame = tk.Frame(master=self)
        toolbar_frame.grid(row=4, columnspan=10, sticky=tk.W)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        return True

    def renew(self):
        self.symbol_selected = self.symbol_list.get_selection()
        self.update()

    def get_data_for_symbol_list(self, parameter):
        self.parameter = parameter
        self.setting_view.update_view(parameter=parameter)
        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history_by_parameter(parameter.id)
        self.symbol_list.update_list(self.symbol_data)