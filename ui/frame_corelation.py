import tkinter as tk
import pandas as pd
import numpy as np
from pandastable import Table, TableModel
from controllers import HistoryController

class CorrelationFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #button2 = tk.Button(self, text="Disagree", command=quit)
        #button2.pack()
        df = self.get_correlation()
        tbM = TableModel(dataframe=df)
        table = Table(self, model=tbM)
        table.show()
        #alter the DataFrame in some way, then update
        table.redraw()

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
            #print(all_base_cuurencies[name].base_currency.name)
            currency_name = all_base_cuurencies[name].base_currency.name
            main_currency_arr = group.ask_price.values
            output_arr = []
            for name2, group2 in historydata_grouped:
                #print(name2)
                #print(all_base_cuurencies[name2].base_currency.name)
                #print(group2)
                tmp_main_currency_arr = main_currency_arr
                current_currency_arr = group2.ask_price.values
                if current_currency_arr.size > main_currency_arr.size:
                    current_currency_arr = np.resize(current_currency_arr, main_currency_arr.shape)
                if current_currency_arr.size < main_currency_arr.size:
                    tmp_main_currency_arr = np.resize(main_currency_arr, current_currency_arr.shape)
                coef = np.corrcoef(tmp_main_currency_arr, current_currency_arr)
                #Pearson correlation coefficient
                #coef is a matrix, here it is matrix 1x1
                output_arr.append(coef[0,1])
            output_pd.loc[currency_name] = output_arr
        return output_pd






#   df = pd.read_sql(sql_command, engine)
