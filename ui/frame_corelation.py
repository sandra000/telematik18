import tkinter as tk
import pandas as pd
import numpy as np
from pandastable import Table, TableModel
from controllers import HistoryController


class CorrelationFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.table = pt = Table(self)
        pt.show()

    def update(self):
        df = self.get_correlation()
        tbm = TableModel(dataframe=df)
        self.table.model = tbm
        self.table.show()
        self.table.redraw()

    def get_correlation(self):
        # TODO: sort the history list
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
                output_arr.append(coef[0, 1])
            output_pd.loc[currency_name] = output_arr
        return output_pd
