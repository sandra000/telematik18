import tkinter as tk
import pandas as pd
import numpy as np
from pandastable import Table, TableModel
from controllers import HistoryController
from ui.components import SettingView, ParameterList


class CorrelationFrame(tk.Frame):
    parameter=None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        history = HistoryController.History()
        self.parameters = history.get_all_parameter_from_history()

        self.setting_view = SettingView(self)
        self.setting_view.grid(row=0, column=1, sticky=(tk.N, tk.E))

        self.parameter_list = ParameterList(self, self.parameters)
        self.parameter_list.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.parameter_list.config(relief=tk.GROOVE, bd=2)
        table_frame = tk.Frame(master=self)
        table_frame.grid(row=0,rowspan=2, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.table = pt = Table(table_frame)
        pt.show()

    def on_show(self):
        self.update()

    def update(self):
        history = HistoryController.History()
        self.parameters = history.get_all_parameter_from_history()
        self.parameter_list = ParameterList(self, self.parameters)
        self.parameter_list.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.parameter_list.config(relief=tk.GROOVE, bd=2)
        df = self.get_correlation()
        tbm = TableModel(dataframe=df)
        if df.empty:
            return True
        self.table.model = tbm
        self.table.show()
        self.table.redraw()

    def get_correlation(self):
        # TODO: sort the history list
        output_pd = pd.DataFrame()
        if not self.parameter:
            return output_pd
        history = HistoryController.History()
        history_data = history.get_all_by_parameter_id(self.parameter.id)

        all_base_cuurencies = history.get_all_base_currency_from_history_by_paramter(self.parameter.id)
        historydata_grouped = history_data.groupby('base_currency_id')
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

    def get_data_for_symbol_list(self, parameter):
        self.parameter = parameter
        self.setting_view.update_view(parameter=parameter)
        df = self.get_correlation()
        tbm = TableModel(dataframe=df)

        self.table.model = tbm
        self.table.show()
        self.table.redraw()