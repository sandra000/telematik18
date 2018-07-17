import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rc
from pandastable import Table, TableModel
from controllers import HistoryController
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import datetime
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, cross_validation, svm
from ui.components import SymbolList
from ui.components import SettingView
from ui.components import ParameterList

#Technical analysts can use autocorrelation to see how much of an impact past prices for a security have on
# its future price
#Assume an investor is looking to discern if a stock's returns in her portfolio exhibit autocorrelation; the
# stock's returns are related to its returns in previous trading sessions. If the returns do exhibit autocorrelation,
# the stock could be characterized as a momentum stock; its past returns seem to influence its future returns.
# The investor runs a regression with two prior trading sessions' returns as the independent variables and the current
# return as the dependent variable. She finds that returns one day prior have a positive autocorrelation of 0.7, while
# the returns two days prior have a positive autocorrelation of 0.3. Past returns seem to influence future returns, and
# she can adjust her portfolio to take advantage of the autocorrelation and resulting momentum.



class LinearRegressionGraphFrame(tk.Frame):
    figureLinearRegressionChart = plt.figure(figsize=(11, 6))
    valor = tk.StringVar()
    plt.rc('font', size=6)
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

        self.a1 = self.figureLinearRegressionChart.add_subplot(331)
        self.a2 = self.figureLinearRegressionChart.add_subplot(332)
        self.a3 = self.figureLinearRegressionChart.add_subplot(333)
        self.a4 = self.figureLinearRegressionChart.add_subplot(334)
        self.a5 = self.figureLinearRegressionChart.add_subplot(335)
        self.a6 = self.figureLinearRegressionChart.add_subplot(336)
        self.a7 = self.figureLinearRegressionChart.add_subplot(337)
        self.a8 = self.figureLinearRegressionChart.add_subplot(338)
        self.a9 = self.figureLinearRegressionChart.add_subplot(339)
        plt.subplots_adjust(left=1, bottom=1, right=1.1, top=1.1,
                        wspace=0.5, hspace=0.5)
        self.canvas = FigureCanvasTkAgg(self.figureLinearRegressionChart, self)
        self.canvas.get_tk_widget().grid(row=1, rowspan=2, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.canvas.draw()

        label = tk.Label(self, text="Linear Regression Price Prediction Charts", font=controller.LARGE_FONT)
        label.grid(row=0, columnspan=12)

        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()

        history = HistoryController.History()
        self.parameters = history.get_all_parameter_from_history()

        self.setting_view = SettingView(self)
        self.setting_view.grid(row=1, column=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        self.parameter_list = ParameterList(self, self.parameters)
        self.parameter_list.grid(row=1, column=11, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.parameter_list.config(relief=tk.GROOVE, bd=2)

        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=2, column=10, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)

        self.forecastOutput = tk.StringVar(self)
        labelForecast = tk.Label(self, textvariable=self.forecastOutput, font=controller.SMALL_FONT)
        labelForecast.grid(row=3, column=10, sticky=(tk.N, tk.S, tk.E, tk.W))

        btn_update_selected = tk.Button(self, text="Update", command=self.renew)
        btn_update_selected.grid(row=4, column=8, columnspan=4)

    def on_show(self):
        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history()
        self.symbol_list = SymbolList(self, self.symbol_data)
        self.symbol_list.grid(row=2, column=10, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.symbol_list.config(relief=tk.GROOVE, bd=2)
        self.forecastOutput.set("")
        self.update()

    def update(self):
        self.a1.cla()
        self.a2.cla()
        self.a3.cla()
        self.a4.cla()
        self.a5.cla()
        self.a6.cla()
        self.a7.cla()
        self.a8.cla()
        self.a9.cla()

        symbol_selected = self.symbol_selected
        history = HistoryController.History()

        if not self.parameter:
            return
        if len(symbol_selected):
            self.setting_view.update_view(parameter=self.parameter, symbols=symbol_selected)
            for item in symbol_selected:
                current_history_data = history.get_by_symbol_id_and_parameter_id(item.id, self.parameter.id)
                #print(current_history_data)
                #df = current_history_data.get_group(bitcoin_name)
                df = current_history_data
                #print(df)
                df['date'] = df['start_time_exchange'].map(mdates.date2num)
                #df = df.loc[df['symbol_id'] == item.id]
                df = df[['ask_price']]

                accuracies = []
                predictions = []

                for x in range(1, 10):
                    forecast_out = int(x)  # predict x days into future
                    df['Prediction'] = df[['ask_price']].shift(-forecast_out)
                    X = np.array(df.drop(['Prediction'], 1))  # labels for linear regression
                    X = preprocessing.scale(X)
                    X_forecast = X[-forecast_out:]
                    X = X[:-forecast_out]

                    y = np.array(df['Prediction'])
                    y = y[:-forecast_out]

                    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

                    # train
                    clf = LinearRegression()
                    clf.fit(X_train, y_train)
                    # test
                    accuracy = clf.score(X_test, y_test)

                    forecast_prediction = clf.predict(X_forecast)

                    accuracies.append(accuracy)
                    predictions.append(forecast_prediction)

        self.a1.scatter([1], predictions[0], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[0]))
        self.a1.set_xticks([1])
        self.a1.set_yticks(predictions[0])
        self.a1.set_title("1 day forecast")

        self.a2.plot([1,2], predictions[1], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[1]))
        self.a2.set_xticks([1,2])
        self.a2.set_yticks(predictions[1])
        self.a2.set_title("2 days forecast")

        self.a3.plot(list(range(1,4)), predictions[2], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[2]))
        self.a3.set_xticks(list(range(1,4)))
        self.a3.set_yticks(predictions[2])
        self.a3.set_title("3 days forecast")

        self.a4.plot(list(range(1,5)), predictions[3], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[3]))
        self.a4.set_xticks(list(range(1,5)))
        self.a4.set_yticks(predictions[3])
        self.a4.set_title("4 days forecast")

        self.a5.plot(list(range(1,6)), predictions[4], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[4]))
        self.a5.set_xticks(list(range(1,6)))
        self.a5.set_yticks(predictions[4])
        self.a5.set_title("5 days forecast")

        self.a6.plot(list(range(1,7)), predictions[5], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[5]))
        self.a6.set_xticks(list(range(1,7)))
        self.a6.set_yticks(predictions[5])
        self.a6.set_title("6 days forecast")

        self.a7.plot(list(range(1,8)), predictions[6], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[6]))
        self.a7.set_xticks(list(range(1,8)))
        self.a7.set_yticks(predictions[6])
        self.a7.set_title("7 days forecast")

        self.a8.plot(list(range(1,9)), predictions[7], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[7]))
        self.a8.set_xticks(list(range(1,9)))
        self.a8.set_yticks(predictions[7])
        self.a8.set_title("8 days forecast")

        self.a9.plot(list(range(1,10)), predictions[8], color='green', label="Confidence: " + "{0:.2f}".format(accuracies[8]))
        self.a9.set_xticks(list(range(1,10)))
        self.a9.set_yticks(predictions[8])
        self.a9.set_title("9 days forecast")

        self.a1.grid(True)
        self.a1.legend()

        self.a2.grid(True)
        self.a2.legend()

        self.a3.grid(True)
        self.a3.legend()

        self.a4.grid(True)
        self.a4.legend()

        self.a5.grid(True)
        self.a5.legend()

        self.a6.grid(True)
        self.a6.legend()

        self.a7.grid(True)
        self.a7.legend()

        self.a8.grid(True)
        self.a8.legend()

        self.a9.grid(True)
        self.a9.legend()


        self.canvas.draw()

        return True

    def renew(self):
        self.symbol_selected = self.symbol_list.get_selection()
        self.update()

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

    def get_data_for_symbol_list(self, parameter):
        self.parameter = parameter
        self.setting_view.update_view(parameter=parameter)
        history = HistoryController.History()
        self.symbol_data = history.get_all_symbol_from_history_by_parameter(parameter.id)
        self.symbol_list.update_list(self.symbol_data)
