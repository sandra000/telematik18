import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from controllers import HistoryController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="BTC Autocorrelation graph\n Time unit is 1 day, lagged by 10 days", font=controller.LARGE_FONT)
        label.pack(pady=5,padx=5)
        self.a = self.figureAutocorrelation.add_subplot(111)

    def on_show(self):
        self.update()

    def update(self):

        #TODO: fix this
        bitcoin_name = 1
        etherum_name = 3
        zcash_name = 17
        history = HistoryController.History() #object for the databank endpoint
        historydata = history.get_all() #dataframe
        if historydata.values.size == 0:
            return
        historydata_grouped = historydata.groupby('base_currency_id')


        ask_price = historydata_grouped.get_group(bitcoin_name).ask_price
        self.a.acorr(ask_price)
        self.a.grid(True)
        self.a.axhline(0, color='black', lw=2)


        canvas = FigureCanvasTkAgg(self.figureAutocorrelation, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        return True
