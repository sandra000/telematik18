import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pandastable import Table, TableModel
from controllers import HistoryController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg


class CorrelationGraphFrame(tk.Frame):
    figureCorelation = plt.figure()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Corelation graph", font=controller.LARGE_FONT)
        label.pack(pady=5,padx=5)
        a = self.figureCorelation.add_subplot(111)

        #TODO: fix this
        bitcoin_name = 1
        etherum_name = 3
        history = HistoryController.History()
        historydata = history.get_all()
        historydata_grouped = historydata.groupby('base_currency_id')
        bitcoin_max_price = historydata_grouped.get_group(bitcoin_name).ask_price.max()
        etherum_max_price = historydata_grouped.get_group(etherum_name).ask_price.max()
        coeficeint_diff = bitcoin_max_price / etherum_max_price
        etherum_ask_price_normalise = historydata_grouped.get_group(etherum_name).ask_price.mul(coeficeint_diff).values
        a.plot(historydata_grouped.get_group(bitcoin_name).ask_price.values, color='red', label='bitcoin')
        a.plot(etherum_ask_price_normalise, color='blue', label='ethereum')
        #plot(bitcoin_name, etherum_name, data=historydata_grouped)
        #matplotlib.pyplot.annotate(*args, **kwargs)
        #matplotlib.pyplot.arrow(x, y, dx, dy, hold=None, **kwargs)¶

        canvas = FigureCanvasTkAgg(self.figureCorelation, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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