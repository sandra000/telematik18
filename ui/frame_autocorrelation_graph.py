import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from controllers import HistoryController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ui.components import SymbolList

# Technical analysts can use autocorrelation to see how much of an impact past prices for a security have on
#  its future price
# Assume an investor is looking to discern if a stock's returns in her portfolio exhibit autocorrelation; the
#  stock's returns are related to its returns in previous trading sessions. If the returns do exhibit autocorrelation,
#  the stock could be characterized as a momentum stock; its past returns seem to influence its future returns.
#  The investor runs a regression with two prior trading sessions' returns as the independent variables and the current
#  return as the dependent variable. She finds that returns one day prior have a positive autocorrelation of 0.7, while
#  the returns two days prior have a positive autocorrelation of 0.3. Past returns seem to influence future returns, and
#  she can adjust her portfolio to take advantage of the autocorrelation and resulting momentum.


class AutocorrelationGraphFrame(tk.Frame):
    figureAutocorrelation = plt.figure()
    valor = tk.StringVar()
    symbol_selected = []

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Set the grid size
        col = 0
        while col < 12:
            self.columnconfigure(col, weight=1)
            col += 1
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        label = tk.Label(self, text="BTC Autocorrelation graph\n Time unit is 1 day, lagged by 10 days", font=controller.LARGE_FONT)
        label.grid(row=0, columnspan=12)
        self.a = self.figureAutocorrelation.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figureAutocorrelation, self)
        self.canvas.get_tk_widget().grid(row=1, rowspan=3, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()
        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=1, column=10, rowspan=3, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)

        btn_update_selected = tk.Button(self, text="Update", command=self.renew)
        btn_update_selected.grid(row=4, column=11)

    def on_show(self):
        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()
        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=1, column=10, rowspan=3, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)
        self.update()

    def update(self):
        self.a.cla()  # which clears data but not axes
        symbol_selected = self.symbol_selected
        history = HistoryController.History()
        if len(symbol_selected):
            for item in symbol_selected:
                current_history_data = history.get_by_symbol_id(item.id)
                current_prices = current_history_data.ask_price
                self.a.acorr(current_prices, label=item.symbol_global_id, usevlines=False)
                self.a.grid(True)
                self.a.axhline(0, color='black', lw=2)

        else:
            bitcoin_name = "BITSTAMP_SPOT_BTC_USD"
            bitcoin_symbol = list(filter(lambda x: x.symbol_global_id == bitcoin_name, self.symbol_data))[0]
            history_data = history.get_by_symbol_id(bitcoin_symbol.id)
            current_prices = history_data.ask_price
            self.a.acorr(current_prices)
            self.a.grid(True)
            self.a.axhline(0, color='black', lw=2)

        self.a.legend()
        self.canvas.draw()

        toolbar_frame = tk.Frame(master=self)
        toolbar_frame.grid(row=4, columnspan=10, sticky=tk.W)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        return True

    def renew(self):
        self.symbol_selected = self.symbol_list.get_selection()
        self.update()

