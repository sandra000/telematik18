import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from controllers import HistoryController, SymbolController
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from sklearn import preprocessing
from ui.components import SymbolList
from ui.components import SettingView
from ui.components import ParameterList


class CorrelationGraphFrame(tk.Frame):
    figureCorelation = plt.figure()
    valor = tk.StringVar()
    test_var = tk.IntVar()
    symbol_selected = []
    parameter = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # set the grid size
        col = 0
        while col < 12:
            self.columnconfigure(col, weight=1)
            col += 1
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=2)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        label = tk.Label(self, text="Correlation graph", font=controller.LARGE_FONT)
        label.grid(row=0, columnspan=12)
        self.type = tk.IntVar(self)
        self.type.set(1)
        tk.Radiobutton(self, text="Normalize to bitcoin course", variable=self.type, value=1).grid(row=3, column=11)
        tk.Radiobutton(self, text="Normalize auto", variable=self.type, value=2).grid(row=4, column=11)

        self.a = self.figureCorelation.add_subplot(111)


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

        self.forecastOutput = tk.StringVar(self)
        labelForecast = tk.Label(self, textvariable=self.forecastOutput, font=controller.LARGE_FONT)
        labelForecast.grid(row=3, column=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        btn_update_selected = tk.Button(self, text="Update", command=self.renew)
        btn_update_selected.grid(row=5, column=11)

    def on_show(self):
        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()
        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=2, column=10, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)
        self.update()

    def update(self):

        self.a.cla()  # which clears data but not axes
        #self.a.clf()  # which clears data and axes

        symbol_selected = self.symbol_selected
        bitcoin_name = "BITSTAMP_SPOT_BTC_USD"

        # for the first time we will compare all currencies with bitcoin as base currency
        base_symbol = list(filter(lambda x: x.symbol_global_id == bitcoin_name, self.symbol_data))[0]

        history = HistoryController.History()

        if not self.parameter:
            return
        # draw base history base currency/symbol data
        history_data = history.get_by_symbol_id_and_parameter_id(base_symbol.id, self.parameter.id)
        if history_data.values.size == 0:
            return
        if self.type.get() == 1:
            self.a.plot(history_data.ask_price.values, color='red', label=bitcoin_name)
            if len(symbol_selected):
                self.setting_view.update_view(parameter=self.parameter, symbols=symbol_selected)
                base_max_price = history_data.ask_price.max()
                for item in symbol_selected:
                    current_history_data = history.get_by_symbol_id_and_parameter_id(item.id, self.parameter.id)
                    current_max_price = current_history_data.ask_price.max()
                    coefficient_diff = base_max_price / current_max_price
                    current_price_normalise = current_history_data.ask_price.mul(coefficient_diff).values
                    self.a.plot(current_price_normalise, label=item.symbol_global_id)
        else:
            if len(symbol_selected):
                self.setting_view.update_view(parameter=self.parameter, symbols=symbol_selected)
                for item in symbol_selected:
                    current_history_data = history.get_by_symbol_id_and_parameter_id(item.id, self.parameter.id)
                    current_price_normalise = self.normalise(current_history_data)
                    self.a.plot(current_price_normalise, label=item.symbol_global_id)

        self.a.legend()

        canvas = FigureCanvasTkAgg(self.figureCorelation, self)
        canvas.get_tk_widget().grid(row=1, rowspan=3, columnspan=10, sticky=(tk.N, tk.S, tk.E, tk.W))
        canvas.draw()

        toolbar_frame = tk.Frame(master=self)
        toolbar_frame.grid(row=5, columnspan=11, sticky=tk.W)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        return True

    @staticmethod
    def normalise(data):
        price_max = data.ask_price.max()
        price_min = data.ask_price.min()
        return np.array(list(map(lambda x: (x-price_min)/(price_max-price_min), data.ask_price.values)))

    def renew(self):
        self.symbol_selected = self.symbol_list.get_selection()
        self.update()

    def get_data_for_symbol_list(self, parameter):
        self.parameter = parameter
        self.setting_view.update_view(parameter=parameter)
        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history_by_parameter(parameter.id)
        self.symbol_list.update_list(self.symbol_data)
